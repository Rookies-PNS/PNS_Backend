from ast import Pass
import email
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class PostForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired()])
    content = TextAreaField('내용', validators=[DataRequired()])

# 계정생성을 위한 폼


class UserCreateForm(FlaskForm):
    userid = StringField('아이디', validators=[
        DataRequired(), Length(min=5, max=20)])  # 길이 5~20
    username = StringField(
        '이름', validators=[DataRequired(), Length(min=2, max=5)])
    password1 = PasswordField(
        '비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])


class UserLoginForm(FlaskForm):
    userid = StringField('아이디', validators=[
                         DataRequired(), Length(min=5, max=20)])
    password = PasswordField('비밀번호', validators=[DataRequired()])
