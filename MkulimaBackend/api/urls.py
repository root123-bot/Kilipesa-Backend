from django.conf.urls import url
from MkulimaBackend.register.views import *
from MkulimaBackend.mkulima.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from MkulimaBackend.mkulima.views import *
from MkulimaBackend.argonomist.views import *
from django.urls import path


urlpatterns = [
    path("password-reset/<str:encoded_pk>/<str:token>/", ResetPassword.as_view(), name='reset-password'),  # Hii baadae tutaibadilisha...
    url(r'password_reset/$', password_reset, name="password_reset_api"),
    url(r'updaterecord/$', update_record, name="update_record"),
    url(r'is_user_active/$', is_user_active, name="is_user_active"),
    url(r'add_record_api/$', add_record_api, name="add_record_api"),
    url(r'change_password/$', change_gpassword, name="change_gpassword"),
    url(r'edit_gatherman_profile/$', edit_gatherman_profile, name="edit_gatherman_profile"),
    url(r'gathered_byme/$', my_info, name="myinfo"),
    url(r'gathermanbio/$', gatherman_bio, name="gatherman_bio"),
    url(r'farmerbio/$', farmer_bio, name="farmer_bio"),
    url(r'user_status/$', user_status, name="user_status"),
    url(r'create_gatherman_profile/$', create_gather_api, name="create_gatherman_api"),
    url(r'farmdetails/$', farm_detail, name="farmdetails"),
    url(r'argodetails/$', argonomist_details, name="argonomist_details"),
    url(r'recomms/$', recomms, name="recommendations"),
    url(r'farms/$', farms, name="farms"),
    url(r'regions/$', mikoa, name="regions"),
    url(r'districts/$', wilaya, name="districts"),
    url(r'addShamba/$', create_shamba, name="create_shamba"),
    url(r'profile/$', user_profile, name="user_profile"),
    url(r'register/$', create_user_api, name='register'),
    url(r'token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]
