# [참고] 점프 투 플라스크
# https://wikidocs.net/book/4542
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

import config
import os

"""
    플라스크(Flask)
    - 마이크로 웹 프레임워크
    - 프레임 워크를 간결하게 유지하고 확장할 수 있다는 의미에서 마이크로라고 부름
    
    플라스크의 확장성 있는 설계
    - 간결하여 무게가 가벼운 만큼 모든 기능을 포함하지 않음
    - 폼(form), 데이터베이스(database)를 처리하는 기능 등을 사용하기 위해 확장 모듈을 추가하며 개발
    
    자유로운 프레임 워크
    - 장고(Django)와 같이 대부분의 프레임워크는 규칙이 복잡하며 그 규칙을 따라야함
    - 플라스크는 최소한의 규칙을 사용
    - 개발의 자유도가 비교적 높음
"""
"""
    플라스크 프로젝트 구조
    ├─ pybo/
    │   ├─ __init__.py
    │   ├─ models.py          # ORM 을 지원하는 SQLAlchemy(모델 기반 데이터베이스 도구) 모델 클래스 정의 파일
    │   ├─ forms.py           # WTForms라는 라이브러리(모델 기반으로 폼 전송)에서 사용될 폼 클래스 정의 파일
    │   ├─ views/             # 화면 구성을 위한 함수 모듈을 저장
    │   │   └─ main_views.py
    │   ├─ static/            # 프로젝트의 스타일시트(css), 자바스크립트(js), 이미지 파일(jpg, png)들을 저장
    │   │   └─ style.css
    │   └─ templates/         # HTML 파일 저장
    │       └─ index.html
    └─ config.py              # 프로젝트 환경설정 파일
"""

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# ORM 에 필요한 전역 객체 생성
# db 객체와 migrate 객체는 다른 모듈들도 쓰기 위해 create_app 함수 밖에서 생성
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))  # db 객체 생성(코드와 DB 를 연결)
# SQLAlchemy
# 파이썬 데이터베이스 도구
# 모델 기반으로 데이터베이스 처리
# 모델 클래스를 정의할 model.py 파일이 필요
migrate = Migrate()  # migrate 객체 생성(클래스 코드를 DB 로 옮겨줌)


# 애플리케이션 팩토리를 위한 함수 생성
def create_app() -> Flask:
    """
    app 객체를 생성하고 요청되는 URL 마다 실행될 수 있는 함수를 포함하여 app 객체 반환

    create_app 함수가 애플리케이션 팩토리로 함수 안에 app 객체를 생성하고 hello_pybo 함수를 포함한다.
    create_app 함수명은 정의된 함수명으로 다른 함수명을 사용하면 정상적으로 작동하지 않는다.

    :return:
    """

    app = Flask(__name__)  # Flask 클래스를 사용하여 플라스크 애플리케이션(app 객체) 생성
    # app 객체를 이용하여 확장 기능 설정
    # app 객체를 전역에서 사용할 경우(create_app 함수 밖) 프로젝트의 규모가 커질수록 순환 참조(circular import)와 같은 오류 발생
    # app 객체를 전역으로 사용할 때 발생하는 문제점은 애플리케이션 팩토리(application factory)를 통해 예방 가능(공식 홈페이지 참고)

    # app configuration
    app.config.from_object(config)  # config.py 파일에 작성한 항목을 읽음

    # ORM
    db.init_app(app)  # init_app 함수를 이용하여 db 객체를 app 에 등록
    migrate.init_app(app, db)  # init_app 함수를 이용하여 migrate 객체를 app 에 등록

    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    from pybo import models

    # blueprint
    # 새로운 URL 매핑이 필요할 때마다 라우팅 함수를 계속 추가해야함
    # 이러한 문제점은 블루프린트(Blueprint)를 사용하여 해결 가능
    # 블루프린트란 URL 과 함수의 매핑을 관리하기 위해 사용하는 도구(클래스)
    from pybo.views import main_views, question_views, answer_views, auth_views
    app.register_blueprint(main_views.bp)  # main_views 모듈의 bp 를 app 의 블루프린트로 등록
    app.register_blueprint(question_views.bp)  # question_views 모듈의 bp 를 app 의 블루프린트로 등록
    app.register_blueprint(answer_views.bp)  # answer_views 모듈의 bp 를 app 의 블루프린트로 등록
    app.register_blueprint(auth_views.bp)  # auth_views 모듈의 bp 를 app 의 블루프린트로 등록

    # filter
    from pybo.filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    # 연습용(사용되지 않는 함수)
    @app.route('/')  # 플라스크 데코레이터
    def hello_pybo() -> str:
        """
        '/' URL 과 매핑되는 라우팅 함수

        @app.route 와 같은 애너테이션으로 URL 을 매핑한다.
        '/' URL 이 요청되면 hello_pybo 함수를 실행한다.
        해당 함수가 적용되기 전 블루프린트가 먼저 등록되었기 때문에 블루프린트의 값으로 사용된다.

        :return:
        """
        return 'Hello, Pybo!'

    return app


if __name__ == '__main__':
    # cmd 창에서 flask 실행
    # 운영 환경에서는 flask run 으로 실행하는 개발서버가 아닌 WSFI 서버로 실행해야 함
    # ```cmd
    # set FLASK_APP=pybo    # FLASK_APP 환경변수에 pybo 값(pybo.py 파일 의미) 설정
    # set FLASK_DEBUG=true  # 디버깅 가능하도록 설정(디버깅 결과의 메시지를 웹 브라우저에 출력)
    # flask run
    # ```
    # flask run 명령어는 반드시 홈디렉토리에서 실행되어야함
    # 파일이 실행되면 main.py 라는 모듈이 실행
    # __name__ 이라는 변수에 "main" 문자열이 담김
    # 서버 실행 중 프로그램을 변경하면 서버가 자동으로 다시 시작하여 변경된 내용을 적용
    # ```

    # ```cmd
    # flask --app pybo --debug run
    # ```
    # --app 옵션: pybo/__init__.py 파일이 FLASK_APP 환경 변수 값이 되도록 설정
    # pybo: pybo/__init__.py 값은 pybo.py 값과 동일하게 pybo 모듈을 의미
    # --debug 옵션: 디버깅 모드 활성화(디버깅 결과의 메시지를 웹 브라우저에 출력)

    # https://stackoverflow.com/questions/19437883/when-scattering-flask-models-runtimeerror-application-not-registered-on-db-w
    # 해당 이유로 디버깅이 안됨 (정확하진 않음)

    a = create_app()

    if os.name == 'nt':
        a.run(debug=True)
    else:
        a.run()
