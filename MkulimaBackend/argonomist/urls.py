from django.conf.urls import url
from .views import *
from django.urls import path

urlpatterns = [
    path('completedtoday/', completed_today, name="completedtoday"),
    path('incomplete/', incomplete_task, name="incomplete"),
    path('editreport/<int:rid>/', edit_report, name="editreport"),
    path('edittest/<int:rid>/', edit_test, name="edittestresults"),
    path('changePassword/', change_password, name="forgotPassword"),
    url(r'editprofile/$', edit_profile, name="editargonomistprofile"),
    path('recommend/<int:rid>/', recommend, name="recommend"),
    path('filltest/<int:rid>/', fill_test, name="filltest"),
    path('assignme/<int:rid>/', assignTaskToMe, name="iwantthistask"),
    url(r'task/$', my_task, name="argontasks"),
    path('testrecord/<int:rid>/', test_record, name="test_record"),
    url(r'addtest/$', add_test, name="argo_addtest"),
    url(r'complete/$', argo_profile, name="argo_profile"),
    url(r'profile/$', access_profile, name="argo_full_profile"),
]
