"""oadb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from django.contrib.auth.decorators import login_required

from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'adapter', views.AdapterViewSet, 'Adapter')
router.register(r'kit', views.KitViewSet, 'Kit')
router.register(r'adapterkit', views.AdapterKitViewSet, 'AdapterKit')
router.register(r'database', views.DatabaseViewSet)
router.register(r'run', views.RunViewSet, 'Run')
router.register(r'runplus', views.RunAdapterViewSet, 'runplus')


urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='oadb-home'),
    url(r'^api/', include(router.urls)),
    url(r'^docs/', include_docs_urls(title='AdapterBase API')),
    url(r'^admin/', views.AdminView.as_view(), name='oadb-admin'),
    url(r'^api-auth/', include('rest_framework.urls')),
]

