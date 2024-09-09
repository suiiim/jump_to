"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # URL을 정규화하는 장고의 기능으로 URL 매핑 시 항상 끝에 슬래쉬를 붙여주는 게 좋음
    path("admin/", admin.site.urls),
    path("pybo/", include("pybo.urls")),  # pybo URL 요청 시 pybo/urls.py 파일의 매핑 정보를 읽어서 처리
    # config 하위의 urls 파일은 프로젝트 단위의 URL 매핑만 추가되어야 함
    # 즉, pybo 로직을 처리할 때마다 config 하위의 urls 파일을 수정하면 안됨
    # pybo 앱 단위의 URL 매핑은 pybo.urls로 변경
]
