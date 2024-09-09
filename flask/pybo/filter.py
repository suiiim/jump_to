import locale

locale.setlocale(locale.LC_ALL, '')  # UnicodeEncodeError 오류가 발생할 때 사용


def format_datetime(value, fmt='%Y년 %m월 %d일 %p %I:%M'):
    """
    날짜 포맷팅 함수

    %Y = 년
    %m = 월
    %d = 일
    %p = AM, PM
    %I = 시간(0~12시로 표현)
    %M = 분

    :param value:
    :param fmt:
    :return:
    """
    return value.strftime(fmt)
