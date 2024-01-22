from django.urls import path
from . import views

app_name = 'captcha'

urlpatterns = [
    path('', views.GenerateCaptchaView.as_view(), name='generate_captcha')
]
