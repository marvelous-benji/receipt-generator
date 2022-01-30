from django.urls import path, re_path

from . import views


urlpatterns = [
    path("signup", views.UserSignup.as_view(), name="usersignup"),
    path("signin", views.UserSignin.as_view(), name="usersignin"),
    re_path(r"^.*/$", views.notfound), # catches all url starting with /api/v1/user_auth but does not hit any endpoint
]
