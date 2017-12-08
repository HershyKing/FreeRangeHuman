"""src URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from dashboard.views import index, url_redirect, splash
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/', include('dashboard.urls'), name='homepage'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^$', splash, name='splash'),
    # url(r'^$', url_redirect, name="url-redirect"),
]

''' django.ontrib.auth.urls imports the following sub urls:

^accounts/login/$ [name='login']
^accounts/logout/$ [name='logout']
^accounts/password_change/$ [name='password_change']
^accounts/password_change/done/$ [name='password_change_done']
^accounts/password_reset/$ [name='password_reset']
^accounts/password_reset/done/$ [name='password_reset_done']
^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$ [name='password_reset_confirm']
^accounts/reset/done/$ [name='password_reset_complete']

'''