from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),  # config/urls.py 파일에서 pybo/가 이미 선언됨
]
