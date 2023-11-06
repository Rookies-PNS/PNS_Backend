import __init__
from flask import Flask, render_template, request, redirect, url_for, session

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
    if request.method == "POST":
        userID = request.form["userID"]
        password = request.form["password"]

    return render_template("auth/login.html")


if __name__ == "__main__":
    app.run(debug=True)
