import os

"""
    ORM (object relational mapping)
    ORM 을 이용하여 파이썬 개발자가 쿼리 작성 없이 데이터 처리 가능
    데이터베이스 종류에 상관 없이 일관된 코드를 유지할 수 있어 유지, 보수하기에 편리함

    example)
    쿼리 이용: INSERT INTO question (subject, content) VALUES ('안녕하세요', '가입 인사드립니다 ^^') ;
    ORM 이용: question = Question(subject='안녕하세요', content='가입 인사드립니다 ^^')
    위의 예제에서는 Question 이라는 파이썬 클래스를 이용하여 SQL 쿼리문을 생성
    Question 은 ORM 클래스로 모델이라고 부름
    
    ORM 라이브러리
    SQLAlchemy 및 Flask-Migrate 라이브러리 사용
    Flask-Migrate 라이브러리를 설치하면 SQLAlchemy 도 함께 설치
    
    Database
    SQLite 데이터베이스 사용
    SQLite 는 주로 소규모 프로젝트에 사용하는 가벼운 파일 기반의 데이터베이스
    실제 운영 시스템에 반영할 때는 규모가 큰 데이터베이스로 교체
"""

"""
    FlaskForm 모듈
    사용자의 정보를 수집하기 위해 해당 정보를 입력 받는 방식을 Form 이라고 함
    Form 을 관리할 수 있는 기능을 제공해주는 패키지로는 Flask-WTF 라이브러리가 있음
    
    Flask-WTF
    [참고] https://flask-wtf.readthedocs.io/en/1.0.x/
    CSRF, Rendering, 파일 업로드 및 reCAPTCHA를 포함한 여러 기능 사용 가능
    특징
        WTForms 와 통합 
        CSRF 토큰으로 보안 양식
        글로벌 CSRF 보호
        reCAPTCHA 지원
        Flask-Uploads 함께 작동하는 파일 업로드 
        Flask-Babel을 사용한 국제화
    
    SECRET_KEY
    CSRF(Cross-Site Request Forgery) 웹 사이트 취약점 공격을 방지하는데 사용
    SECRET_KEY 를 기반으로 생성된 CSRF 토큰으로 실제 웹 페이지에서 작성된 데이터인지 판단
    CSRF 토큰은 CSRF 를 방어하기 위해 생성하는 무작위 문자열
    
    # CSRF: 사용자의 요청을 위조하는 웹 사이트 공격 기법
"""

BASE_DIR = os.path.dirname(__file__)  # 현재 디렉토리 경로

# 데이터베이스 파일은 프로젝트 홈 디렉토리 하위에 pybo.db 파일로 저장됨
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))  # 데이터베이스 접속 주소
SQLALCHEMY_TRACK_MODIFICATIONS = False  # SQLAlchemy 이벤트 처리 옵션 비활성화

SECRET_KEY = "dev"
