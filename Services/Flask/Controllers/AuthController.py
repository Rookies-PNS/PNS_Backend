from datetime import datetime
from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from bod import db
from bod.forms import UserCreateForm, UserLoginForm
from bod.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(userid=form.userid.data).first()
        if not user:
            user = User(userid=form.userid.data,
                        username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        phonenum=form.phonenum.data,
                        email=form.email.data,
                        create_date=datetime.now())
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        # sql의 select
        user = User.query.filter_by(userid=form.userid.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.userid
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)


# 로그인 여부 확인
# 하단의 애너테이션이 적용된 함수는 모든(다른 파일포함) 라우팅 함수보다 항상 먼저 실행된다
@bp.before_app_request
def load_logged_in_user():
    # g의 의미는 global이며 전역적으로 사용되는 개체이다
    # request 변수처럼 요청/응답 과정에서 유효하다
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        # 기본키를 파라미터로 전역개체 g.user에 user객체를 가져옴
        g.user = User.query.get(user_id)
