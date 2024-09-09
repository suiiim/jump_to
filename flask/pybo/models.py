# https://docs.sqlalchemy.org/en/13/core/type_basics.html
from pybo import db

# __init__.py 파일에서 생성한 ASLAlchemy 클래스 객체


"""
    Question 모델 사용법

    질문 및 답변 저장
    >>> q = Question(subject='pybo가 무엇인가요?', content='pybo에 대해서 알고 싶습니다.', create_date=datetime.now())
    >>> db.session.add(q)
    >>> a = Answer(question=q, content='네 자동으로 생성됩니다.', create_date=datetime.now())
    >>> db.session.add(a)
    >>> db.session.rollback() # 롤백하면 저장 안됨
    >>> db.session.commit() # 롤백 없이 커밋하면 저장됨

    질문 조회
    >>> q.id
    1
    >>> Question.query.all()
    [<Question 1>]

    질문 수정
    >>> q = Question.query.get(1)
    >>> q
    <Question 2>
    >>> q.subject = 'Flask Model Question'
    >>> db.session.commit()

    참조 및 역 참조 조회
    >>> a.question
    <Question 2>
    >>> q.answer_set
    [<Answer 1>]

    질문 삭제
    >>> q = Question.query.get(1)
    >>> db.session.delete(q)
    >>> db.session.commit()
"""


class Question(db.Model):  # db.Model 클래스 상속
    # attribute
    id = db.Column(db.Integer, primary_key=True)  # 고유 번호
    subject = db.Column(db.String(200), nullable=False)  # 제목
    content = db.Column(db.Text(), nullable=False)  # 내용
    create_date = db.Column(db.DateTime(), nullable=False)  # 작성 일시


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 고유 번호
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))  # question 테이블(Question 클래스)의 id
    question = db.relationship('Question', backref=db.backref('answer_set'))  # 역참조
    content = db.Column(db.Text(), nullable=False)  # 내용
    create_date = db.Column(db.DateTime(), nullable=False)  # 작성 일시


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 고유 번호
    username = db.Column(db.String(150), unique=True, nullable=False)  # 사용자명
    password = db.Column(db.String(200), nullable=False)  # 비밀번호
    email = db.Column(db.String(120), unique=True, nullable=False)  # 이메일


"""
    db.Column
    첫 번째 인수
        속성에 저장할 데이터 타입
    두 번재 인수
        primary_key: 기본키, 중복된 값을 가질 수 없음
        nullable: 빈값 허용 여부
        db.ForeignKey: 외부키, 기존 모델과 연결된 속성
        unique: 같은 값 저장 불가능

    db.ForeignKey
    첫 번째 인수
        기존 모델과 연결한 외부 모델의 속성
    두 번째 인수
        ondelete -> CASCADE: 삭제 연동 설정; 질문이 삭제되면 질문에 달린 답변도 같이 삭제됨

    db.relationship
    첫 번째 인수
        참조할 모델명
    두 번째 인수
        backref: 역참조 설정; 질문에서 답변을 역참조할 수 있음
"""
