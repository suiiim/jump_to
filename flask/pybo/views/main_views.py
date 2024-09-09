from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect

from pybo.models import Question

bp = Blueprint(name='main', import_name=__name__, url_prefix='/')  # 블루프린트 객체 생성


# name: main 은 블루프린트의 별칭이며 나중에 url_for 함수에 자주 사용될 예정
# import_name: __name__ 변수에는 모듈명인 main_views 가 인수로 전달
# url_prefix: 기본적으로 붙일 접두어 URL

@bp.route('/')
def index():
    """
    '/' URL로 매핑되면 /question/list 함수로 리다이렉트되는 라우팅 함수

    redirect 함수를 이용하여 해당 URL로 페이지로 리다이렉트

    url_for 함수를 이용하여 라우팅 함수에 매핑되어 있는 URL을 리턴
    question(블루프린트 별칭) -> _list(함수명) 순서로 해석되어 라우팅 함수를 찾음
    url_for 함수를 사용하면 유지·보수하기 쉬워짐

    :return:
    """
    return redirect(url_for('question._list'))


@bp.route('/hello')
def hello_pybo():
    """
    '/hello' URL 과 매핑되는 라우팅 함수

    __init__.py 파일에 있던 hello_pybo 함수와 동일한 값을 반환하지만 매핑되는 URL 이 달라졌다.
    애너테이션이 @bp.route 로 변경되었다.

    :return:
    """
    return 'Hello, Pybo!'


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    """
    질문 ID 값을 매개변수로 받아 해당 ID 의 질문을 나타내는 HTML 을 전달하는 라우팅 함수

    데코레이터의 URL 매핑 규칙에 있는 int:question_id 는 question_id 에 int 타입이 매핑된다는 의미
    URL 에 있는 <int:question_id> 값은 question_id 값으로 전달
    question_id 에 해당되는 질문이 없을 경우 404 에러 출력

    example)
    http://localhost:5000/detail/1/
    Flask Model Question
    pybo에 대해서 알고 싶습니다.
    http://localhost:5000/detail/2/
    Not Found
    The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.

    :param question_id: int
    :return:
    """
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question)
