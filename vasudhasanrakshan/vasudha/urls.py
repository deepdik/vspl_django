"""vasudha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import url,include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import activate
from django.views.generic.base import TemplateView
from rest_framework_jwt.views import (
    refresh_jwt_token,
    obtain_jwt_token,
    verify_jwt_token
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/v1/users/',include(('accounts.api.urls','accounts'),namespace="users-api")),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),#Email Activation

    url('^', include('django.contrib.auth.urls')), # email varification
    url(r'^rest-auth/', include('rest_auth.urls')), # social login
    url(r'^accounts/',include('allauth.urls'), name='socialaccount_signup'),
      
]


urlpatterns += [
    url(r'',TemplateView.as_view(template_name='social.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

