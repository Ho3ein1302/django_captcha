from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.UserView.as_view(), name='users_list'),
    path('register/', views.UserRegister.as_view())
]
