from django.urls import path

from . import views


urlpatterns = [
    path('user_auth/signup/', views.UserSignup.as_view(), name='usersignup'),
    path('user_auth/signin/', views.UserSignin.as_view(), name='usersignin'),
]
