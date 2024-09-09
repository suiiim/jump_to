from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

"""
    Cookie & Session
    웹 프로그램은 [웹 브라우저 요청 → 서버 응답] 순서로 실행되며, 서버 응답이 완료되면 웹 브라우저와 서버 사이의 네트워크 연결은 끊어진다. 
    하지만 수 많은 브라우저가 서버에 요청할 때마다 매번 새로운 세션이 생성되는 것이 아니라 동일한 브라우저의 요청에서 서버는 동일한 세션을 사용한다.

    그렇다면 서버는 도대체 어떻게 웹 브라우저와 연결 고리(세션)를 맺는걸까?

    그 해답은 쿠키(Cookie)에 있다. 
    쿠키는 서버가 웹 브라우저에 발행하는 값이다. 
    웹 브라우저가 서버에 어떤 요청을 하면 서버는 쿠키를 생성하여 전송하는 방식으로 응답한다. 
    그러면 웹 브라우저는 서버에서 받은 쿠키를 저장한다. 
    이후 서버에 다시 요청을 보낼 때는 저장한 쿠키를 HTTP 헤더에 담아서 전송한다. 
    그러면 서버는 웹 브라우저가 보낸 쿠키를 이전에 발행했던 쿠키값과 비교하여 같은 웹 브라우저에서 요청한 것인지 아닌지를 구분할 수 있다. 
    이때 세션은 바로 쿠키 1개당 생성되는 서버의 메모리 공간이라고 할 수 있다.
"""

bp = Blueprint('auth', __name__, url_prefix='/auth')  # /auth/ URL로 호출되는 블루프린트 객체 생성


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()

    if request.method == 'POST' and form.validate_on_submit():  # POST 방식 및 form 데이터가 정합한지 확인
        # POST 방식
        # 계정 저장 로직 수행
        user = User.query.filter_by(username=form.USERNAME.data).first()  # username 데이터 조회
        if not user:
            # 등록되지 않은 사용자일 경우 계정 저장
            user = User(username=form.USERNAME.data,
                        password=generate_password_hash(form.PASSWORD1.data),  # 해쉬로 암호화(복호화 불가능)
                        email=form.EMAIL.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            # 등록된 사용자
            flash('이미 존재하는 사용자입니다.')

    # GET 방식
    # 계정 등록 화면 출력
    return render_template('auth/signup.html', form=form)


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        # POST 방식
        # 로그인
        error = None
        user = User.query.filter_by(username=form.USERNAME.data).first()
        if not user:  # 사용자 존재 여부 확인
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.PASSWORD.data):  # DB 의 비밀번호와 일치 여부 확인
            error = "비밀번호가 올바르지 않습니다."
        if error is None:  # 에러가 없으면 로그인 성공
            session.clear()
            session['user_id'] = user.id
            # 세션 삭제 후 새로운 사용자 정보 저장하면서 로그인
            # 세션 객체는 플라스크에서 제공
            # 한번 생성하면 그 값을 계속 유지
            # 즉, 서버에 브라우저별로 생성되며 메모리에 저장됨
            # URL 요청할 때마다 객체를 생성하는 request 객체와 다름
            return redirect(url_for('main.index'))
        flash(error)

    # GET 방식
    return render_template('auth/login.html', form=form)


@bp.before_app_request  # 라우팅 전 사용되는 애너테이션
def load_logged_in_user():
    """
    모든 라우팅(URL 호출) 전 실행되는 함수

    플라스트 변수인 g 를 이용하여 user 정보를 확인한다.
    세션에 저장된 user_id 를 확인하고 값이 있을 경우 g.user 값에 User 객체를 저장한다.
    g.user 를 이용하여 username, email 과 같은 사용자 정보를 확인할 수 있다.

    :return:
    """

    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/logout/')
def logout():
    """
    세션을 삭제하는 함수

    :return:
    """
    session.clear()  # 세션의 모든 값을 삭제
    # 세션이 삭제되면 g.user 값도 None 으로 삭제됨
    return redirect(url_for('main.index'))
