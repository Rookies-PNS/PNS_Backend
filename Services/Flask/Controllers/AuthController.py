from typing import Optional
from flask import Blueprint, redirect, render_template, request, url_for, flash, session
from werkzeug.utils import redirect

from Domains.Entities import UserVO, SimpleUser
from Applications.Usecases.UserServices import CreateUserService, LoginService
from Infrastructures.IOC import get_user_storage, get_post_storage
from Applications.Results import (
    Result,
    Fail,
    Fail_CreateUser_IDAlreadyExists,
    Fail_CheckUser_PasswardNotCorrect,
    Fail_CheckUser_IDNotFound,
)
from Services.Flask.Models import user_to_dict
from Services.Flask.Views.forms import UserCreateForm, UserLoginForm, PasswordChangeForm
from icecream import ic

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/signup/", methods=("GET", "POST"))
def signup():
    form = UserCreateForm()
    if request.method == "POST" and form.validate_on_submit():
        service = CreateUserService(get_user_storage())
        match service.create(
            form.account.data, form.password1.data, form.name.data, form.nickname.data
        ):
            case user if isinstance(user, SimpleUser):
                return redirect(url_for("auth.login"))
            case Fail(type=type) if type == Fail_CreateUser_IDAlreadyExists.type:
                flash("이미 존재하는 사용자 입니다.")
            case Fail(type=type) if type == "Fail_CreateUser_Invalid_Password":
                ic()
                flash("""비밀번호 필수 사항) 1. 최소 8자 이상의 길이 2. 대소문자, 숫자, 특수문자를 혼용""")
            case Fail(type=type):
                ic()
                ic(type, "NotImplementedError")
            case _:
                pass

    return render_template("auth/signup.html", form=form)


@bp.route("/login/", methods=("GET", "POST"))
def login():
    form = UserLoginForm()
    if request.method == "POST" and form.validate_on_submit():
        (repoW, repoR) = get_user_storage()
        service = LoginService(repoR, repoW)  # DB 미구현
        match service.login(form.userid.data, form.password.data):
            case user if isinstance(user, SimpleUser):
                session.clear()
                session["user"] = user
                return redirect(url_for("main.index"))
            case Fail(type=type) if type == Fail_CheckUser_IDNotFound.type:
                flash("존재하지 않는 사용자입니다.")
            case Fail(type=type) if type == Fail_CheckUser_PasswardNotCorrect.type:
                flash("비밀번호가 올바르지 않습니다.")
            case Fail(type=type):
                ic()
                ic(type, "NotImplementedError")
            case _:
                pass
    return render_template("auth/login.html", form=form)


@bp.route("/signup_success/")
def signup_success():
    return render_template("auth/signup_success.html")
