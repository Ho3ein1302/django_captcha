from django.urls import path
from . import views

urlpatterns = [
    path('', views.GenerateCaptchaView.as_view(), name='generate_captcha')
]
