import __init__
from flask import Flask, render_template, request, redirect, url_for, session

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


# Routing
@app.route("/")
def home():
    return render_template("home/home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    from icecream import ic

    if request.method == "POST":
        ic()
        login = LoginUser(get_user_storage())
        userID = request.form["userID"]
        password = request.form["password"]
        ic(userID, password)
        user = login.login(userID, password)
        ic(user)
        ic(isinstance(user, UserVO))
        match user:
            case _ if isinstance(user, UserVO):
                session.permanent = True
                session["user_id"] = userID
                return render_template("home/home.html")
            case _ if isinstance(user, Fail):
                pass

    return render_template("auth/login.html")


if __name__ == "__main__":
    app.run(debug=True)
