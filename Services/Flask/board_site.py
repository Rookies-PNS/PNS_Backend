import __init__
from flask import Flask, render_template, request, redirect, url_for, session

from Services import get_secrets_key

# APP init
app = Flask(__name__, static_url_path="/static", static_folder="static")
app.secret_key = get_secrets_key()


# Routing
@app.route("/")
def home():
    return render_template("home/home.html")


if __name__ == "__main__":
    app.run(debug=True)
