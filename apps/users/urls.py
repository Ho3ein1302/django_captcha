from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('users/', views.UserView.as_view(), name='users_list'),
    path('register/', views.UserRegister.as_view(), name='user_register'),
    path('login/', views.UserLogin.as_view(), name='user_login'),
    path('logout/', views.UserLogOut.as_view(), name='user_logout'),
    path('refresh/', views.GetNewRefreshToken.as_view(), name='get_new_refresh_token'),
]
