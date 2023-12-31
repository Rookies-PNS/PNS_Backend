from ast import Pass
import email
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, PasswordField, FileField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, PasswordField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class PostForm(FlaskForm):
    subject = StringField("제목", validators=[DataRequired()])
    content = TextAreaField("내용", validators=[DataRequired()])
    image = FileField(
        "이미지 업로드",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "png"], "JPG와 PNG 이미지만 업로드 가능합니다."),
        ],
    )
    image = FileField(
        "이미지 업로드",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "png"], "JPG와 PNG 이미지만 업로드 가능합니다."),
        ],
    )


# 계정생성을 위한 폼


class UserCreateForm(FlaskForm):
    account = StringField(
        "아이디", validators=[DataRequired(), Length(min=5, max=20)]
    )  # 길이 5~20
    name = StringField("이름", validators=[DataRequired(), Length(min=2, max=35)])
    nickname = StringField("닉네임", validators=[DataRequired(), Length(min=2, max=20)])
    password1 = PasswordField(
        "비밀번호", validators=[DataRequired(), EqualTo("password2", "비밀번호가 일치하지 않습니다")]
    )
    password2 = PasswordField("비밀번호확인", validators=[DataRequired()])


class UserLoginForm(FlaskForm):
    userid = StringField("아이디", validators=[DataRequired(), Length(min=5, max=20)])
    password = PasswordField("비밀번호", validators=[DataRequired()])


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField("현재 비밀번호", validators=[DataRequired()])
    new_password1 = PasswordField(
        "새 비밀번호",
        validators=[DataRequired(), EqualTo("new_password2", "새 비밀번호가 일치하지 않습니다")],
    )
    new_password2 = PasswordField("새 비밀번호 확인", validators=[DataRequired()])
