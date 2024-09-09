from datetime import datetime

from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import AnswerForm
from pybo.models import Question, Answer

# 답변 블루프린트
bp = Blueprint('answer', __name__, url_prefix='/answer')


@bp.route('/create/<int:question_id>', methods=('POST',))  # POST 페이지 요청 받음
def create(question_id):
    """
    /answer/create/<int:question_id>/ URL 의 페이지를 요청받으면 답변 생성 후 상세 화면으로 이동하기 위해 리다이렉트 /question/detail/<int:question_id>/

    :param question_id:
    :return:
    """
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)  # question 테이블의 id 가 없으면 Not Found 페이지 전달

    # POST 방식에서 정합성만 검사
    if form.validate_on_submit():  # form 데이터가 정합한지 확인
        content = request.form['content']  # 폼으로 전송된 데이터 중 content 값을 content 에 저장

        answer = Answer(content=content, create_date=datetime.now())
        question.answer_set.append(answer)  # 질문에 달린 답변들
        #  Question과 Answer 모델이 연결되어 있어 backref에 설정한 answer_set를 사용할 수 있다고 설명했었음
        # 위와 동일
        # answer = Answer(question=question, content=content, create_date=datetime.now())
        # db.session.add(answer)
        db.session.commit()

        return redirect(url_for('question.detail', question_id=question_id))

    return render_template('question/question_detail.html', question=question, form=form)
