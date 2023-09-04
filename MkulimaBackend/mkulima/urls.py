from .views import *
from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^underreview/$', TemplateView.as_view(
        template_name="mkulima/inactiveaccount.html"), name='waitingverification')
]
