import __init__
from flask import Flask, render_template, request, session, redirect, url_for

from Domains.Entities import UserVO
from Applications.Usecases import LoginUser
from Applications.Results import Fail, Result

from Infrastructures.IOC import get_user_storage
from Services import get_secrets_key

# APP init
app = Flask(
    __name__,
    static_url_path="/Views/static",
    static_folder="Views/static",
    template_folder="Views/templates",
)
app.secret_key = get_secrets_key()

# Content Security Policy 설정
csp_header = {
    "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self';"
}


# Routing
@app.route("/")
def home():
    return render_template("home/home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = LoginUser(get_user_storage())
        userID = request.form["userID"]
        password = request.form["password"]
        user: UserVO = login.login(userID, password)
        match user:
            case _ if isinstance(user, UserVO):
                session.permanent = True
                session["user_id"] = user.name  # 딕셔너리
                return redirect(url_for("home"))
            case _ if isinstance(user, Fail):
                pass

    return render_template("auth/login.html")


@app.route("/logout")
def logout():
    # 로그아웃 처리: 세션에서 'user_id'와 'username' 제거
    session.pop("user_id", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
