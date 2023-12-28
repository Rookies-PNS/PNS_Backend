from flask import Blueprint, redirect, render_template, request, url_for, session, flash
from werkzeug.utils import redirect
from werkzeug.datastructures import MultiDict
from Commons import PostId

from Domains.Entities import Post, PostVO, SimplePost, SimpleUser
from Applications.Usecases import (
    GetPostList,
    GetPost,
    CreatePost,
    DeletePost,
    UpdatePost,
)
from Applications.Results import Result, Fail
from Infrastructures.IOC import get_user_storage, get_post_storage

from Services.Flask.Models import post_to_dict, posts_to_dicts, dict_to_user
from Services.Flask.Views.forms import PostForm

from icecream import ic

bp = Blueprint("post", __name__, url_prefix="/post")


@bp.route("/list/<int:page>")
def _list(page):
    posts_per_page = 10
    page = max(page, 1)
    serivce = GetPostList(get_post_storage())
    post_list = posts_to_dicts(serivce.get_list_no_filter(page - 1, posts_per_page))

    create_auth = False
    if "user" in session:
        user = dict_to_user(session["user"])
        create_auth = CreatePost(get_post_storage(), get_user_storage()).check_auth(
            user
        )

    if page > 1 and len(post_list) == 0:  # 넘치는 페이지를 요청할 경우
        return redirect(
            url_for(
                "post._list", page=page - 1, start_page=(int(page) <= 1), end_page=True
            )
        )
    elif 0 < len(post_list) < posts_per_page:  # 넘치는 페이지를 요청할 경우
        return render_template(
            "post/post_list.html",
            post_list=post_list,
            page=page,
            start_page=(int(page) <= 1),
            end_page=True,
            create_auth=create_auth,
        )
    else:  # 정상 요청
        return render_template(
            "post/post_list.html",
            post_list=post_list,
            page=page,
            start_page=(int(page) <= 1),
            end_page=False,
            create_auth=create_auth,
        )


@bp.route("/detail/<int:post_id>/")
def detail(post_id):
    service = GetPost(get_post_storage())
    match service.get_post_from_post_id(post_id):
        case post if isinstance(post, PostVO):
            auth = post.get_uid() is None
            update_auth, delete_auth = False, False
            if not auth and "user" in session:
                user = dict_to_user(session["user"])
                update_auth = DeletePost(
                    get_post_storage(), get_user_storage()
                ).check_auth(post, user)
                delete_auth = UpdatePost(
                    get_post_storage(), get_user_storage()
                ).check_auth(post, user)
                ic(user, delete_auth, update_auth)
            post = post_to_dict(post)
            return render_template(
                "post/post_detail.html",
                post=post,
                delete_auth=delete_auth,
                update_auth=update_auth,
            )
        case _:
            return redirect(url_for("post._list", page=1))


@bp.route("/create/", methods=("GET", "POST"))
def create():
    create_auth = False
    if "user" in session:
        user = dict_to_user(session["user"])
        create_auth = CreatePost(get_post_storage(), get_user_storage()).check_auth(
            user
        )
    if not create_auth:
        return redirect(url_for("post._list", page=1))

    form = PostForm()
    if request.method == "POST" and form.validate_on_submit():
        service = CreatePost(get_post_storage(), get_user_storage())
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

    return render_template("post/post_form.html", form=form)


@bp.route("/delete/<int:post_id>/", methods=["Get", "POST"])
def delete(post_id):
    if "user" in session:
        user = dict_to_user(session["user"])
    else:
        user = None

    match GetPost(get_post_storage()).get_post_from_post_id(post_id):
        case post if isinstance(post, PostVO):
            service = DeletePost(get_post_storage(), get_user_storage())
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
    return redirect(url_for("post.detail", post_id=post_id))


@bp.route("/update/<int:post_id>/", methods=("GET", "POST"))
def update(post_id):
    post = GetPost(get_post_storage()).get_post_from_post_id(post_id)

    if isinstance(post.user, SimpleUser) and "user" in session:
        user = dict_to_user(session["user"])
        if not user.check_equal_uid(post.user.uid):
            flash("수정 권한이 없습니다.")
            return redirect(url_for("post.detail", post_id=post_id, auth=False))
    else:
        user = None
    # form = PostForm(formdata=MultiDict({'subject':post.get_title(), 'content':post.get_content()}))
    # form = PostForm(subject=post.get_title(), content=post.get_content())

    form = PostForm()
    if request.method == "POST" and form.validate_on_submit():
        service = UpdatePost(get_post_storage(), get_user_storage())
        match service.update(post, form.subject.data, form.content.data, user=user):
            case post if isinstance(post, SimplePost):
                return redirect(url_for("main.index", post_id=post_id))
            case Fail(type=type) if type == "Fail_UpdatePost_UserMismatch":
                flash("수정 권한이 없습니다.")
                return redirect(url_for("post.detail", post_id=post_id))
            case Fail(type=type):
                ic()
                ic(type, "NotImplementedError")
            case _:
                pass

    form.subject.data = post.get_title()
    form.content.data = post.get_content()
    # return render_template('post/post_edit.html', form=form, subject=post.get_title(), content=post.get_content())
    return render_template("post/post_edit.html", form=form)
