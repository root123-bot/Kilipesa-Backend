from .views import *
from django.conf.urls import url
from django.urls import path

urlpatterns = [
    url(r'addedtodayrecords/$', added_today, name="addedtodayrecords"),
    url(r'changePassword/$', change_password, name="gatherman_changepassword"),
    url(r'editprofile/$', edit_profile, name="gather_edit_profile"),
    path('editrecord/<int:rid>/', edit_record, name="editrecord"),
    url(r'addrecord/$', create_record, name="gather_add_record"),
    url(r'complete/$', access_profile, name="gather_full_profile"),
    url(r'addprofile/$', gather_profile, name="gather_profile")
]
