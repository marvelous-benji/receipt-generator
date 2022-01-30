"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from config.settings.mysettings import get_enviroment_variable
from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


@api_view(["GET"])
def documenter(request):
    '''
    Forces django to redirect to documentation url
    when root url is clicked
    '''

    return redirect(get_enviroment_variable("DOCUMENTER_URL"))


@api_view(["GET", "POST", "PUT", "DELETE"])
def notfound(request):
    '''
    Forces django to return json url not found response rather than
    spawning HTML 404 error(when DEBUG=True) or blank 500 error(when DEBUG=False)
    '''

    return Response(
        {
            "status": "failed",
            "msg": "URL was not found on the server, check your spelling",
        },
        status=status.HTTP_404_NOT_FOUND,
    )


urlpatterns = [
    # path('admin/', admin.site.urls), commented out as it's not needed
    path("", documenter),
    path("api/v1/user_auth/", include("MyUser.urls")),
    path("api/v1/receipt/", include("Receipt.urls")),
    re_path(r"^.*/$", notfound), # catches all urls that does not startwith api/v1
]
