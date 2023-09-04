"""MkulimaBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from MkulimaBackend.api import urls as api_urls
from MkulimaBackend.argonomist import urls as argo_urls
from MkulimaBackend.mkulima import urls as mkulima_urls
from MkulimaBackend.gatherman import urls as gather_urls
from MkulimaBackend.administrator import urls as administrator_urls
from MkulimaBackend.mkulima.views import *
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from MkulimaBackend.mkulima.views import mail


urlpatterns = [
    url(r'^sendmail/$', mail, name="sendmail"),
    url(r'^measure/$', TemplateView.as_view(template_name='measure.html'), name="measure"),
    url(r'^login/$', login_view, name="login"),
    url(r'^register/$', create_user, name="jisajili"),
    url(r'^api/', include(api_urls)),
    url(r'^argo/', include(argo_urls)),
    url(r'^administrator/', include(administrator_urls)),
    url(r'^mkulima/', include(mkulima_urls)),
    url(r'^gather/', include(gather_urls)),
    url(r'^logout/$', logoutuser, name="logout"),
    url(r'^about/$', about_view, name="about"),
    url(r'^$', index_view, name="localhost"),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='mkulima/password_reset.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='mkulima/password_reset_sent.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='mkulima/password_reset_form.html'), name="password_reset_confirm"), # this is used on posting data i think so...
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='mkulima/password_reset_complete.html'), name="password_reset_complete"),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
