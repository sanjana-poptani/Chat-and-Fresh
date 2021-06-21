from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home,name="home"),
    path('',views.login,name="login"),
    path('register/',views.register,name="register"),
    path('token/',views.token_send,name="token_send"),
    path('success/',views.success,name="success"),
    path('verify/<auth_token>',views.verify,name="verify"),
    path('error/',views.error_page,name="error"),
    path('change_pwd/<token>/',views.change_pwd,name="change_pwd"),
    path('forgot_pwd/',views.forgot_pwd,name="forgot_pwd"),
    path('logout/',views.logout,name="logout"),
]
