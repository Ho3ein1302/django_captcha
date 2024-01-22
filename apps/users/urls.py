from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.UserView.as_view(), name='users_list'),
    path('register/', views.UserRegister.as_view()),
    path('login/', views.UserLogin.as_view()),
    path('logout/', views.UserLogOut.as_view()),
    path('refresh/', views.GetNewRefreshToken.as_view()),
]
