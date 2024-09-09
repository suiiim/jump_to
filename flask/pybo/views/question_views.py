from flask import Blueprint, render_template, request, url_for
from datetime import datetime
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question
from pybo.forms import QuestionForm, AnswerForm

bp = Blueprint(name='question', import_name=__name__, url_prefix='/question')  # 블루프린트 객체 생성


# name: 블루프린트 별칭
# import_name: __name__ 변수에는 모듈명인 question_views 가 인수로 전달
# url_prefix: URL 접두어로 '/question' 이 항상 사용됨

@bp.route('/list/')
def _list():
    """
    '/question/list/' URL 과 매핑되는 라우팅 함수

    질문 목록 기능에 해당하는 함수명을 list가 아니라 _list로 지정한 이유는 list가 파이썬의 예약어이기 때문이다.
    question 테이블의 create_date 를 내림차순으로 정렬한 값을 받아 html 페이지에 전달

    템플릿 파일
    파이썬 문법을 사용할 수 있는 HTML 파일

    :return:
    """
    page = request.args.get('page', type=int, default=1)  # 페이징 구현
    # GET 방식의 URL 을 요청할 때 int 타입의 page 파라미터를 사용해야하며 default 값을 1 로 사용한다는 의미

    question_list = Question.query.order_by(Question.create_date.desc())  # 작성일시를 역순으로 정렬한 질문 리스트
    question_list = question_list.paginate(page=page, per_page=10)  # 리스트 10개씩 페이징 적용
    # paginate 함수 속성
    # items: 현재 페이지에 해당하는 게시물 리스트
    # total: 게시물 전체 개수
    # per_page: 페이지당 보여 줄 게시물 개수
    # page: 현재 페이지 번호
    # iter_pages: 페이지 범위
    # prev_num / next_num: 이전 페이지 번호 / 다음 페이지 번호
    # has_prev / has_next: 이전 페이지 존재 여부 / 다음 페이지 존재 여부

    return render_template('question/question_list.html', question_list=question_list)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)  # question 테이블의 id 가 없으면 Not Found 페이지 전달
    # 이동할 홈페이지, 질문 리스트, 폼 데이터 3개의 값을 render_template 함수를 이용하여 전송
    return render_template('question/question_detail.html', question=question, form=form)


@bp.route('/create/', methods=('GET', 'POST'))  # 별도의 method 속성이 지정되지 않으면 GET 방식으로 처리
def create():
    """
    GET 요청이 오면 question_form 페이지로 이동하고 POST 요청이 오면 폼 데이터에 이상이 없을 경우 질문 저장 후 main.index 페이지로 이동

    폼 데이터의 "제목" 데이터는 form.subject.data, "내용" 데이터는 form.content.data 로 받음

    :return:
    """
    form = QuestionForm()
    # POST 방식
    if request.method == 'POST' and form.validate_on_submit():  # 전송된 API 방식이 POST 이며 전송된 폼 데이터가 정합한지 확인
        # validate_on_submit 함수에서 수행되는 정합성 검사는 QuestionForm 의 속성에서 지정한 검증 도구들을 이용하여 확인
        question = Question(subject=form.SUBJECT.data, content=form.CONTENT.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    # GET 방식
    return render_template('question/question_form.html', form=form)
