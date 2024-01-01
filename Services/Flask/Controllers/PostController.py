from flask import Blueprint, redirect, render_template, request, url_for, session, flash
from werkzeug.utils import redirect
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

from Services.Flask.Models import post_to_dict, posts_to_dicts, dict_to_user
from Services.Flask.Views.forms import PostForm

from icecream import ic

bp = Blueprint("post", __name__, url_prefix="/post")


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
    create_auth = False
    if "user" in session:
        user = dict_to_user(session["user"])
        create_auth = (get_post_storage(), get_user_storage()).check_auth(user)
    if not create_auth:
        return redirect(url_for("post._list", page=1))

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

    return render_template("post/private_post_form.html", form=form)


@bp.route("/delete/<int:post_id>/", methods=["Get", "POST"])
def delete(post_id):
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
    return redirect(url_for("post.detail", post_id=post_id))


@bp.route("/update/<int:post_id>/", methods=("GET", "POST"))
def private_update(post_id):
    post = GetPrivatePostService(get_post_storage()).get_post_detail(post_id)

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
        service = UpdatePostService(get_post_storage(), get_user_storage())
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
            get_post_storage(), get_user_storage()
        ).check_auth(user)

    return render_template(
        "post/public_post_list.html",
        post_list=post_list,
        page=page,
    )
