import __init__

from flask import Flask, Blueprint, url_for, session
from werkzeug.utils import redirect
from flask_wtf import CSRFProtect
from Services import get_secrets_key
from Services.Flask.Controllers import (
    AuthController,
    PostController,
)

flask_path = __init__.root_path / "Services" / "Flask"
# APP init
app = Flask(
    __name__,
    static_folder= str(flask_path/"Views"/"static"),
    template_folder=str(flask_path/"Views/templates"),
)
app.secret_key = get_secrets_key()
csrf = CSRFProtect(app)


main_bp = Blueprint('main', __name__, url_prefix='/')

@main_bp.route('/')
def index():
    session.clear()
    return redirect(url_for('auth.login', page=1))

app.register_blueprint(main_bp)
app.register_blueprint(AuthController.bp)
app.register_blueprint(PostController.bp)
# app.register_blueprint(CommentController.bp)

if __name__ == "__main__":
    app.run(debug=True)
