from django.urls import path

from . import views


urlpatterns = [
    path('signup', views.UserSignup.as_view(), name='usersignup'),
    path('signin', views.UserSignin.as_view(), name='usersignin'),
]
