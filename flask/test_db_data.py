from pybo import db, create_app
from pybo.models import Question
from datetime import datetime


def create_db_data_total(num: int):
    app = create_app()
    app.app_context().push()
    db.create_all()
    for i in range(num):
        q = Question(subject='테스트 데이터입니다.:[%03d]' % i, content='-', create_date=datetime.now())
        db.session.add(q)
    db.session.commit()


if __name__ == '__main__':
    create_db_data_total(300)
