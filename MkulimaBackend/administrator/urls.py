
from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
    path('taarifashamba/<int:fid>/', farm_info, name="shamba_info"),  # we pass farm_id
    path('enableuser/<int:uid>/<slug:type>/', enable_user, name="enableuser"),
    path('disableuser/<int:uid>/<slug:type>/', disable_user, name="disableuser"),
    path('deletenoti/<int:nid>/', del_notification, name="deletenotification"),
    path('markasread/<int:nid>/', mark_notification_as_read, name="markasread"),
    path('viewnoti/<int:nid>/', view_noti, name="view_notification"),
    url(r'notification_center/$', notification_center, name="notificationcenter"),
    path('viewfarmerinfo/<int:fid>/', view_farmer_info, name="viewfarmerinfo"),
    path('viewgatherprofile/<int:gid>/',
         view_gatherprofile, name="viewgatherprofile"),
    path('viewargoprofile/<int:aid>/', view_profile, name="viewargoprofile"),
    url(r'soilreport/$', test_results, name="soilreport"),
    url(r'cultivation/$', cultivation, name="cultivation"),
    url(r'recommendedseed/$', seed_amount, name="seedamount"),
    url(r'recommendedcrops/$', recommended_crops, name="recommendedcrops"),
    url(r'yieldreport/$', yield_report, name="yieldreport"),
    url(r'fertilizerreport/$', fertilizer_report, name="fertlizerreport"),
    url(r'farmersreport/$', farmer_report, name="farmersreport"),
    url(r'farmreport/$', farms_report, name="farmsreport"),
    path('deleteinfo/<int:rid>/', delete_info, name="deleteinfo"),
    path('deletereport/<int:rid>/', drop_report, name="deletereport"),
    path('deletegather/<int:pid>/', ad_del_gather, name="admindelgather"),
    path('deleteargo/<int:pid>/', ad_del_argo, name="admindelargo"),
    path('viewgather/<int:gid>/', view_gather, name="indigather"),
    path('viewargo/<int:gid>/', view_argo, name="indiargo"),
    url(r'testsrecomms/$', testsrecoms, name="testandrecomms"),
    url(r'reports/crops/$', crops, name="cropsreport"),
    url(r'info/farms/$', farms, name="farms"),
    url(r'^user/gatherman/filter/$', gather_by_year, name="gatherbyyear"),
    url(r'^user/gatherman/check/$', gather_status, name="gatherstatus"),
    url(r'^user/gatherman/month/$', gather_month, name="filtergatherbymonth"),
    url(r'^user/argonomist/month/$', month_filter, name="filterbymonth"),
    url(r'^user/argonomist/filter/$', year_filter, name="filterbyyear"),
    url(r'^user/argonomist/check/$', argonomist_status, name="status"),
    url(r'^$', home_view, name="administrator"),
    url(r'^user/argonomist/$', argonomist, name="userargonomist"),
    url(r'^user/gatherman/$', gatherman, name="usergatherman")
]
