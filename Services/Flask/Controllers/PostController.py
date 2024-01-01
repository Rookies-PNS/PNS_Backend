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
from Infrastructures.MySQL.Storages import MySqlIImageWriteableStorage
from Services.Flask.Models import post_to_dict, posts_to_dicts, dict_to_user
from Services.Flask.Views.forms import PostForm, ImageUploadForm

from icecream import ic
import os

bp = Blueprint("post", __name__, url_prefix="/post")
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(
    "PNS_Backend", "Services", "Flask", "Views", "templates", "post", "uploads"
)


@bp.route("/prlist/<int:page>")
def private_list(page):
    posts_per_page = 10
    page = max(page, 1)
    serivce = GetPrivatePostService(None)  # get_post_storage
    post_list = posts_to_dicts(serivce.get_post_list(page - 1, posts_per_page))
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
    service = GetPrivatePostService(None)  # get_post_storage()
    match service.get_post_detail(post_id):
        case post if isinstance(post, PostVO):
            auth = post.get_uid() is None
            update_auth, delete_auth = False, False
            if not auth and "user" in session:
                user = dict_to_user(session["user"])
                update_auth = UpdatePostService(
                    get_post_storage(), get_user_storage()
                ).check_auth(post, user)
                delete_auth = DeletePostService(
                    get_post_storage(), get_user_storage()
                ).check_auth(post, user)
                ic(user, delete_auth, update_auth)
            post = post_to_dict(post)
            return render_template(
                "post/private_post_detail.html",
                post=post,
                delete_auth=delete_auth,
                update_auth=update_auth,
            )
        case _:
            return redirect(url_for("post._prlist", page=1))


@bp.route("/prcreate/", methods=("GET", "POST"))
def private_create():
    create_auth = True
    if "user" in session:
        user = dict_to_user(session["user"])
        create_auth = (get_post_storage(), get_user_storage()).check_auth(user)
    if not create_auth:
        return redirect(url_for("post.private_list", page=1))

    form = PostForm()
    form2 = ImageUploadForm()
    if request.method == "POST":
        if form.validate_on_submit() and form2.validate_on_submit():
            service = CreatePostService(get_post_storage(), get_user_storage())
            if "user" in session:
                user = dict_to_user(session["user"])
            else:
                user = None
            match service.create(form.subject.data, form.content.data, user=user):
                case post if isinstance(post, SimplePost):
                    return redirect(url_for("main.index"))
                case Fail(type=type):
                    ic()
                    ic(type, "NotImplementedError")
                case _:
                    ic()
                    pass

            if form2.validate_on_submit():
                # 이미지 파일 처리
                image_file = form2.image.data
                filename = secure_filename(image_file.filename)  # 파일 이름 보안 처리
                object_name = f"Image-logs/{filename}"  # 저장할 경로와 파일 이름 설정

                # S3에 업로드를 위한 스토리지 인스턴스 생성
                storage = MySqlIImageWriteableStorage()
                if storage.upload_to_s3(image_file, "pns-bucket", object_name):
                    image_url = storage.get_s3_url("pns-bucket", object_name)

                    # 이미지 URL 데이터베이스에 저장
                    user_id = current_user.id
                    if storage.save_image_data(image_url, user_id):
                        flash("이미지가 업로드되었습니다.", "success")
                    else:
                        flash("이미지 저장 실패.", "error")
                    return redirect(url_for("post.private_create"))

    return render_template("post/private_post_form.html", form=form, form2=form2)


@bp.route("/prdelete/<int:post_id>/", methods=["Get", "POST"])
def private_delete(post_id):
    if "user" in session:
        user = dict_to_user(session["user"])
    else:
        user = None

    match GetPrivatePostService(get_post_storage()).get_post_detail(post_id):
        case post if isinstance(post, PostVO):
            service = DeletePostService(get_post_storage(), get_user_storage())
            match service.delete(post, user):
                case id if isinstance(id, PostId):
                    return redirect(url_for("main.index", page=1))
                case Fail(type=type) if type == "Fail_DeletePost_UserMismatch":
                    flash("삭제 권한이 없습니다.")
                case Fail(type=type):
                    ic()
                    ic(type, "NotImplementedError")
                case _:
                    ic()
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
    posts_per_page = 10
    page = max(page, 1)
    serivce = GetPublicPostService(None)  # get_post_storage
    post_list = posts_to_dicts(serivce.get_list_no_filter(page - 1, posts_per_page))
    create_auth = False
    if "user" in session:
        user = dict_to_user(session["user"])
        create_auth = CreatePostService(
            # get_post_storage(), get_user_storage()
            None,
            None,
        ).check_auth(user)

    return render_template(
        "post/public_post_list.html",
        post_list=post_list,
        page=page,
    )


@bp.route("/pbdetail/<int:post_id>/")
def public_detail(post_id):
    service = GetPublicPostService(None)  # get_post_storage()
    match service.get_post_from_post_id(post_id):
        case post if isinstance(post, PostVO):
            auth = post.get_uid() is None
            update_auth, delete_auth = False, False
            if not auth and "user" in session:
                user = dict_to_user(session["user"])
                update_auth = UpdatePostService(
                    # get_post_storage(), get_user_storage()
                    None,
                    None,
                ).check_auth(post, user)
                delete_auth = DeletePostService(
                    # get_post_storage(), get_user_storage()
                    None,
                    None,
                ).check_auth(post, user)
                ic(user, delete_auth, update_auth)
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
    if "user" in session:
        user = dict_to_user(session["user"])
        create_auth = (get_post_storage(), get_user_storage()).check_auth(user)
    if not create_auth:
        return redirect(url_for("post.public_list", page=1))

    form = PostForm()
    if request.method == "POST" and form.validate_on_submit():
        service = CreatePostService(get_post_storage(), get_user_storage())
        if "user" in session:
            user = dict_to_user(session["user"])
        else:
            user = None
        match service.create(form.subject.data, form.content.data, user=user):
            case post if isinstance(post, SimplePost):
                return redirect(url_for("main.index"))
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


@app.route("/upload_image", methods=["GET", "POST"])
def upload_image():
    form = ImageUploadForm()
    if form.validate_on_submit():
        # 이미지 파일 처리
        image_file = form.image.data
        filename = secure_filename(image_file.filename)  # 파일 이름 보안 처리
        object_name = f"Image-logs/{filename}"  # 저장할 경로와 파일 이름 설정

        # S3에 업로드를 위한 스토리지 인스턴스 생성
        storage = MySqlIImageWriteableStorage()
        if storage.upload_to_s3(image_file, "pns-bucket", object_name):
            image_url = storage.get_s3_url("pns-bucket", object_name)

            # 이미지 URL 데이터베이스에 저장
            user_id = current_user.id
            if storage.save_image_data(image_url, user_id):
                flash("이미지가 업로드되었습니다.", "success")
            else:
                flash("이미지 저장 실패.", "error")
            return redirect(url_for("post.private_create"))

    return render_template("upload_image.html", form=form)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    form = ImageUploadForm()
    if form.validate_on_submit():
        # 이미지 처리 로직
        flash("이미지가 업로드되었습니다.")
        return redirect(url_for("index"))
    return render_template("upload.html", form=form)
