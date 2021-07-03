from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home,name="home"),
    path('home/<int:sender>/<int:receiver>/', views.message_view, name='rooms'),
    path('home1/',views.home1,name="home1"),
    path('chatroom/<int:sender>/<int:receiver>/', views.msge_view, name='rooms1'),
    path('api/messages/<int:sender>/<int:receiver>/', views.message_list, name='message-detail'),
    path('api/messages/', views.message_list, name='message-list'),
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
