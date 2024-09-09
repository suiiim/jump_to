[점프 투 장고](https://wikidocs.net/book/4223)

# 0장 들어가기 전에

## 파이썬 버전과 장고 버전

| 장고 버전 | 사용 가능한 파이썬 버전                         |
|-------|---------------------------------------|
| 3.0   | 3.6, 3.7, 3.8, 3.9                    |
| 3.1   | 3.6, 3.7, 3.8, 3.9                    |
| 3.2   | 3.6, 3.7, 3.8, 3.9, 3.10              |
| 4.0   | 3.8, 3.9, 3.10                        |
| 4.1   | 3.8, 3.9, 3.10, 3.11 (added in 4.1.3) |
| 4.2   | 3.8, 3.9, 3.10, 3.11                  |
| 5.0   | 3.10, 3.11, 3.12                      |

# 1장 장고 개발 준비!

## Django (장고)

![장고 슬로건](https://wikidocs.net/images/page/78004/O_1-01_3.png)
 
- The web framework for perfectionists with deadlines.
- 마감에 쫓기는 완벽주의자를 위한 웹 프레임워크
- 마감 기한이 있어도 완벽하게 만들 수 있다는 의미

> Web Framework (웹 프레임워크)
> 웹 프로그램을 만들기 위한 도구 모음
> 쿠키나 세션, 로그인/로그아웃, 권한, 데이터베이스 처리 등을 쉽고 빠르게 만들 수 있도록 도와줌

### 장고의 특징

1. 튼튼한 보안
   - SQL 인젝션, XSS, CSRF, 클릭재킹과 같은 보안 공격을 기본적으로 막아줌
2. 무수히 많은 기능
   - 2005년부터 기능이 추가되고 다듬어짐 

### 장고 프로젝트 생성 및 시작

```shell
django-admin startproject config .
```

- 현재 디렉토리에 프로젝트를 생성 
- 현재 디렉토리에 config라는 앱 디렉토리가 생성 
- 장고가 필요로 하는 여러 디렉터리와 파일들이 생성됨 
  - `conf/settings.py`
    - 장고 설정 파일
    - `LANGUAGE_CODE`: en-us -> ko-kr
    - `TIME_ZONE`: UTC -> Asia/Seoul
  - `conf/urls.py`
    - URL 요청에 대한 응답 위치 매핑
    - 페이지 요청이 발생하면 가장 먼처 호출되는 파일 

```shell
python manage.py runserver
```

- 장고 서버가 시작
- http://127.0.0.1:8000/ URL로 접속 가능

# 2장 장고의 기본 요소 익히기!

## App (앱)

```shell
django-admin startapp pybo
```

- `startapp` 명령어를 이용하여 `pybo` 앱 생성
- 현재 디렉토리 하위에 pybo라는 디렉토리가 생성됨 
  - `pybo/views.py`
    - Response 함수 작성 

## 장고 개발 흐름

![기본 흐름](https://wikidocs.net/images/page/70649/2-01_6.png)

1. 브라우저에서 로컬 서버로 http://localhost:8000/pybo 페이지 요청
2. urls.py 파일에서 /pybo URL 매핑을 확인 후 views.py 파일의 index 함수 호출
3. 호출한 결과를 브라우저에 반영
