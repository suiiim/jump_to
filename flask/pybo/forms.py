from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

"""
    Flask-WTF 라이브러리 사용하여 FlaskForm 관리 
"""


class QuestionForm(FlaskForm):  # FlaskForm 을 상속한 QuestionForm 클래스 생성
    SUBJECT = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])  # 글자수 제한 O
    CONTENT = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])  # 글자수 제한 X

    # String, Text 와 같은 폼의 속성을 정의
    # [참고] https://wtforms.readthedocs.io/en/2.3.x/fields/#basic-fields
    # raw_data: Form Label -> '제목' 또는 '내용' 이라는 라벨 출력
    # validators: 검증을 위해 사용되는 도구 -> DataRequired(필수 항목 확인), Email(이메일 확인), Length(길이 확인) 등 존재
    # [참고] https://wtforms.readthedocs.io/en/2.3.x/validators/#built-in-validators


class AnswerForm(FlaskForm):
    CONTENT = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])


class UserCreateForm(FlaskForm):  # 계정 생성을 위한 Form 클래스
    USERNAME = StringField('사용자이름', validators=[
        DataRequired(),
        Length(min=3, max=25)  # 3-25 사이의 길이
    ])
    # 비밀번호가 정확한지 확인하기 위해 2개의 비밀번호 필드(password1, password2) 사용
    PASSWORD1 = PasswordField('비밀번호', validators=[
        DataRequired(),
        EqualTo('PASSWORD2', '비밀번호가 일치하지 않습니다')  # password2 와 항상 동일하여야 함
    ])
    PASSWORD2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    # 이메일 필드
    EMAIL = EmailField('이메일', validators=[
        DataRequired(),
        Email()  # 이메일 검증 조건
    ])

    # Email() 함수를 사용하기 위해서 email-validator 설치 필요
    # -> pip install email_validator


class UserLoginForm(FlaskForm): # 로그인 수행을 위한 Form 클래스
    USERNAME = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    PASSWORD = PasswordField('비밀번호', validators=[DataRequired()])
