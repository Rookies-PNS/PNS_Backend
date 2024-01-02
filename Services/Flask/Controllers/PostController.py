from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
    session,
    flash,
    jsonify,
    Flask,
)
from flask_login import current_user
from werkzeug.utils import redirect, secure_filename
from werkzeug.datastructures import MultiDict
from Commons import PostId

from Domains.Entities import Post, PostVO, SimplePost, SimpleUser
from Applications.Usecases.PostServices import (
    CreatePostService,
    DeletePostService,
    GetPrivatePostService,
    GetPublicPostService,
    UpdatePostService,
)
from Applications.Results import Result, Fail
from Infrastructures.IOC import get_user_storage, get_post_storage
from Infrastructures.MySQL.Storages.MySqlIImageWriteableStorage import (
    MySqlIImageWritableStorage,
)
from Services.Flask.Models import post_to_dict, posts_to_dicts, dict_to_user
from Services.Flask.Views.forms import PostForm, ImageUploadForm

from datetime import datetime
from icecream import ic
import os

bp = Blueprint("post", __name__, url_prefix="/post")
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(
    "PNS_Backend", "Services", "Flask", "Views", "templates", "post", "uploads"
)


@bp.route("/prlist/<int:page>")
def private_list(page):
    if "user" in session:
        user = dict_to_user(session["user"])
    else:
        user = None
        return redirect(url_for("auth.login"))

    posts_per_page = 10
    page = max(page, 1)
    serivce = GetPrivatePostService(get_post_storage()[1])  # get_post_storage
    post_list = posts_to_dicts(serivce.get_post_list(user, page - 1, posts_per_page))
    create_auth = False
    if "user" in session:
        user = dict_to_user(session["user"])
        create_auth = CreatePostService(
            get_post_storage(), get_user_storage()
        ).check_auth(user)
    return render_template(
        "post/private_post_list.html",
        post_list=post_list,
        page=page,
    )


@bp.route("/prdetail/<int:post_id>/")
def private_detail(post_id):
    if "user" in session:
        user = dict_to_user(session["user"])
    else:
        return redirect(url_for("post.Private_list", page=1))
    service = GetPrivatePostService(get_post_storage()[1])  # get_post_storage()
    (PW, PR) = get_post_storage()
    (UW, UR) = get_user_storage()
    match service.get_post_detail(user, post_id):
        case post if isinstance(post, PostVO):
            auth = post.get_uid() is None
            update_auth, delete_auth = False, False
            if not auth and "user" in session:
                user = dict_to_user(session["user"])
                update_auth = UpdatePostService(PW, UR).check_auth(post, user)
                delete_auth = DeletePostService(PW, PR, UR).check_auth_coms(
                    user, post.owner, post.share_flag
                )
                ic(user, delete_auth, update_auth)
            post = post_to_dict(post)
            return render_template(
                "post/private_post_detail.html",
                post=post,
                delete_auth=delete_auth,
                update_auth=update_auth,
            )
        case _:
            return redirect(url_for("post.private_list", page=1))


@bp.route("/prcreate/", methods=("GET", "POST"))
def private_create():
    create_auth = False
    post_service = CreatePostService(get_post_storage()[0], get_user_storage()[0])
    if "user" in session:
        user = dict_to_user(session["user"])
        create_auth = post_service.check_auth(user)
    if not create_auth:
        return redirect(url_for("post.private_list", page=1))

    form = PostForm()
    form2 = ImageUploadForm()
    ic()
    if request.method == "POST":
        ic()
        if form.validate_on_submit() or form2.validate_on_submit():
            ic()
            if "user" in session:
                user = dict_to_user(session["user"])
            else:
                user = None
            ic()
            if form2.validate_on_submit():
                # 이미지 파일 처리
                ic()
                image_file = form2.image.data
                ic(image_file)
                filename = secure_filename(image_file.filename)  # 파일 이름 보안 처리
                object_name = f"Image-logs/{filename}"  # 저장할 경로와 파일 이름 설정

                # S3에 업로드를 위한 스토리지 인스턴스 생성
                storage = MySqlIImageWritableStorage()
                if storage.upload_to_s3(image_file, "pns-bucket", object_name):
                    image_url = storage.get_s3_url("pns-bucket", object_name)

                    # 이미지 URL 데이터베이스에 저장
                    user_id = current_user.id
                    if storage.save_image_data(image_url, user_id):
                        flash("이미지가 업로드되었습니다.", "success")
                    else:
                        flash("이미지 저장 실패.", "error")
                    return redirect(url_for("post.private_create"))
            match post_service.create(
                form.subject.data,
                form.content.data,
                user=user,
                share_flag=False,
                target_time=datetime.now(),
                img=None,
            ):
                case none if none is None:
                    return redirect(url_for("post.private_list", page=1))
                case Fail(type=type):
                    ic()
                    ic(type, "NotImplementedError")
                case _:
                    ic()
                    pass

    return render_template("post/private_post_form.html", form=form, form2=form2)


@bp.route("/private_delete/<int:post_id>/", methods=["Get", "POST"])
def private_delete(post_id):
    ic()
    if "user" in session:
        user = dict_to_user(session["user"])
    else:
        user = None
        return redirect(url_for("post.private_detail", post_id=post_id))

    (PW, PR) = get_post_storage()
    (UW, UR) = get_user_storage()
    service = DeletePostService(PW, PR, UR)

    if not service.check_auth(user, post_id):
        flash("삭제할 수 없습니다.")
    else:
        match service.delete(user, post_id):
            case none if none is None:
                ic(none)
                return redirect(url_for("post.public_list", page=1))
            case fail:
                ic(fail)
                flash("삭제할 수 없습니다.")

    return redirect(url_for("post.private_detail", post_id=post_id))


@bp.route("/prupdate/<int:post_id>/", methods=("GET", "POST"))
def private_update(post_id):
    post = GetPrivatePostService(get_post_storage()).get_post_detail(post_id)

    if isinstance(post.user, SimpleUser) and "user" in session:
        user = dict_to_user(session["user"])
        if not user.check_equal_uid(post.user.uid):
            flash("수정 권한이 없습니다.")
            return redirect(url_for("post.private_detail", post_id=post_id, auth=False))
    else:
        user = None
    # form = PostForm(formdata=MultiDict({'subject':post.get_title(), 'content':post.get_content()}))
    # form = PostForm(subject=post.get_title(), content=post.get_content())

    form = PostForm()
    if request.method == "POST" and form.validate_on_submit():
        service = UpdatePostService(get_post_storage(), get_user_storage())
        match service.update(post, form.subject.data, form.content.data, user=user):
            case post if isinstance(post, SimplePost):
                return redirect(url_for("main.index", post_id=post_id))
            case Fail(type=type) if type == "Fail_UpdatePost_UserMismatch":
                flash("수정 권한이 없습니다.")
                return redirect(url_for("post.private_detail", post_id=post_id))
            case Fail(type=type):
                ic()
                ic(type, "NotImplementedError")
            case _:
                pass

    form.subject.data = post.get_title()
    form.content.data = post.get_content()
    # return render_template('post/post_edit.html', form=form, subject=post.get_title(), content=post.get_content())
    return render_template("post/private_post_edit.html", form=form)


@bp.route("/prdetail/<int:post_id>/set_public", methods=["POST"])
def private_set_public(post_id):
    # 여기에 실제 데이터베이스를 업데이트하는 코드가 들어가야 합니다.
    # 예: post = Post.query.get(post_id)
    #     post.is_public = True
    #     db.session.commit()

    # 데이터베이스 업데이트 성공 시 메시지 반환
    return jsonify(
        {"status": "success", "message": "일기가 공개상태가 되었습니다.", "post_id": post_id}
    )


@bp.route("/prdetail/<int:post_id>/set_private", methods=["POST"])
def private_set_private(post_id):
    # 여기에 실제 데이터베이스를 업데이트하는 코드가 들어가야 합니다.
    # 예: post = Post.query.get(post_id)
    #     post.is_public = False
    #     db.session.commit()

    # 데이터베이스 업데이트 성공 시 메시지 반환
    return jsonify(
        {"status": "success", "message": "일기가 비공개상태가 되었습니다.", "post_id": post_id}
    )


@bp.route("/pblist/<int:page>")
def public_list(page):
    if "user" in session:
        user = dict_to_user(session["user"])
    else:
        user = None
        return redirect(url_for("auth.login"))
    posts_per_page = 10
    page = max(page, 1)
    serivce = GetPublicPostService(get_post_storage()[1])  # get_post_storage
    post_list = posts_to_dicts(serivce.get_post_list(user, page - 1, posts_per_page))
    create_auth = False
    if "user" in session:
        user = dict_to_user(session["user"])
        create_auth = CreatePostService(
            get_post_storage(), get_user_storage()
        ).check_auth(user)

    return render_template(
        "post/public_post_list.html",
        post_list=post_list,
        page=page,
    )


@bp.route("/pbdetail/<int:post_id>/")
def public_detail(post_id):
    if "user" in session:
        user = dict_to_user(session["user"])
    else:
        user = None
        return redirect(url_for("post.public_list", page=1))

    service = GetPublicPostService(get_post_storage()[1])  # get_post_storage()

    (PW, PR) = get_post_storage()
    (UW, UR) = get_user_storage()
    match service.get_post_detail(user, post_id):
        case post if isinstance(post, PostVO):
            auth = post.get_uid() is None
            update_auth, delete_auth = False, False
            if not auth and "user" in session:
                user = dict_to_user(session["user"])
                update_auth = UpdatePostService(PW, UR).check_auth(post, user)
                delete_auth = DeletePostService(PW, PR, UR).check_auth_coms(
                    user, post.owner, post.share_flag
                )
            post = post_to_dict(post)
            return render_template(
                "post/public_post_detail.html",
                post=post,
                delete_auth=delete_auth,
                update_auth=update_auth,
            )
        case _:
            return redirect(url_for("post._pblist", page=1))


@bp.route("/pbcreate/", methods=("GET", "POST"))
def public_create():
    create_auth = False
    service = CreatePostService(get_post_storage()[0], get_user_storage()[1])
    if "user" in session:
        user = dict_to_user(session["user"])
        create_auth = service.check_auth(user)
    if not create_auth:
        return redirect(url_for("post.public_list", page=1))

    form = PostForm()
    if request.method == "POST" and form.validate_on_submit():
        if "user" in session:
            user = dict_to_user(session["user"])
        else:
            user = None
        match service.create(
            form.subject.data,
            form.content.data,
            user=user,
            share_flag=True,
            target_time=datetime.now(),
            img=None,
        ):
            case none if none is None:
                return redirect(url_for("post.public_list", page=1))
            case Fail(type=type):
                ic()
                ic(type, "NotImplementedError")
            case _:
                ic()
                pass

    return render_template("post/public_post_form.html", form=form)


@bp.route("/pbupdate/<int:post_id>/", methods=("GET", "POST"))
def public_update(post_id):
    post = GetPrivatePostService(get_post_storage()).get_post_from_post_id(post_id)

    if isinstance(post.user, SimpleUser) and "user" in session:
        user = dict_to_user(session["user"])
        if not user.check_equal_uid(post.user.uid):
            flash("수정 권한이 없습니다.")
            return redirect(url_for("post.public_detail", post_id=post_id, auth=False))
    else:
        user = None
    # form = PostForm(formdata=MultiDict({'subject':post.get_title(), 'content':post.get_content()}))
    # form = PostForm(subject=post.get_title(), content=post.get_content())

    form = PostForm()
    if request.method == "POST" and form.validate_on_submit():
        service = UpdatePostService(get_post_storage(), get_user_storage())
        match service.update(post, form.subject.data, form.content.data, user=user):
            case post if isinstance(post, SimplePost):
                return redirect(url_for("main.index", post_id=post_id))
            case Fail(type=type) if type == "Fail_UpdatePost_UserMismatch":
                flash("수정 권한이 없습니다.")
                return redirect(url_for("post.public_detail", post_id=post_id))
            case Fail(type=type):
                ic()
                ic(type, "NotImplementedError")
            case _:
                pass

    form.subject.data = post.get_title()
    form.content.data = post.get_content()
    # return render_template('post/post_edit.html', form=form, subject=post.get_title(), content=post.get_content())
    return render_template("post/public_post_edit.html", form=form)


@bp.route("/pbdetail/<int:post_id>/set_private", methods=["POST"])
def public_set_private(post_id):
    # 여기에 실제 데이터베이스를 업데이트하는 코드가 들어가야 합니다.
    # 예: post = Post.query.get(post_id)
    #     post.is_public = False
    #     db.session.commit()

    # 데이터베이스 업데이트 성공 시 메시지 반환
    return jsonify(
        {"status": "success", "message": "일기가 비공개상태가 되었습니다.", "post_id": post_id}
    )
