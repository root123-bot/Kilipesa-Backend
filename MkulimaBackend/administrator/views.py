from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from MkulimaBackend.mkulima.models import *
import json
import sys
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files import File
from MkulimaBackend.utils.index import notificationsByUser
from django.shortcuts import resolve_url


def not_viewed_notifications(user):
    notifications = notificationsByUser(user.id)
    notification_length = 0
    # only show the number of notification which is not viewed yet..
    for notification in notifications:
        if notification.isViewed:
            continue
        notification_length += 1
    
    return notification_length

class EnableUser(View):
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['uid']
        type = self.kwargs['type']
        user = get_user_model().objects.get(id=user_id)
        user.is_active = True
        user.save()
        if (type == "Argonomist"):
            # viewargoprofile
            return HttpResponseRedirect(resolve_url('viewargoprofile', aid=user.argonomic.id))

        if (type == "Gatherman"):
            return HttpResponseRedirect(resolve_url('viewgatherprofile', gid=user.gather.id))

enable_user = EnableUser.as_view()


class DisableUser(View):
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['uid']
        type = self.kwargs['type']
        user = get_user_model().objects.get(id=user_id)
        user.is_active = False
        user.save()
        if (type == "Argonomist"):
            return HttpResponseRedirect(resolve_url('viewargoprofile', aid=user.argonomic.id))

        if (type == "Gatherman"):
            return HttpResponseRedirect(resolve_url('viewgatherprofile', gid=user.gather.id))

disable_user = DisableUser.as_view()

class DeleteNotification(View):
    def get(self, request, *args, **kwargs):
        print('im executed...')
        notification_id = self.kwargs['nid']
        notification = Notification.objects.get(id=notification_id)
        print('notification to delete ', notification)
        notification.delete()
        return HttpResponseRedirect(reverse('notificationcenter'))

del_notification = DeleteNotification.as_view()

class MarkNotificationAsRead(View):
    def get(self, request, *args, **kwargs):
        notification_id = self.kwargs['nid']
        notification = Notification.objects.get(id=notification_id)
        notification.isViewed = True
        notification.save()
        return HttpResponseRedirect(reverse('notificationcenter'))

mark_notification_as_read = MarkNotificationAsRead.as_view()

class ViewGivenNotification(View):
    template_name = "administrator/viewnotification.html"

    @method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        notification_id = self.kwargs['nid']
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        lname = ""
        user_group = "admin"
        notification = Notification.objects.get(id=notification_id)
        notification.isViewed = True
        notification.save()
        created_user_group = ""
        argo_id = None
        gather_id = None
        if notification.created_user:
            user = get_user_model().objects.get(id=int(notification.created_user))
            
            if hasattr(user, 'gather'):
                created_user_group = "Gatherman"
                gather_id = user.gather.id
            if hasattr(user, 'argonomic'):
                created_user_group = "Argonomist"
                argo_id = user.argonomic.id
                
        return render(request, self.template_name, {"created_user_group": created_user_group, "argo_id":  argo_id, "gather_id": gather_id, "user_created": created_user_group, "notification": notification, "usergroup": user_group, "fname": name,
                                                    "lname": lname, "photo": photo})


view_noti = ViewGivenNotification.as_view()

class NotificationCenter(View):
    template_name = "administrator/notification.html"

    @method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        lname = ""
        user_group = "admin"
        notifications = notificationsByUser(user.id)
        noti = notificationsByUser(user.id)
        idadi_noti = len(list(noti))
        return render(request, self.template_name, {"idadi": idadi_noti, "notifications": notifications, "usergroup": user_group, "fname": name,
                                                    "lname": lname, "photo": photo})


notification_center = NotificationCenter.as_view()

class ViewFarmInfo(View):
    template_name = "administrator/viewfarminfo.html"

    @method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print('im executed')
        farm_id = self.kwargs['fid']
        farm = Farm.objects.get(id=farm_id)
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        lname = ""
        user_group = "admin"
        not_viewed = not_viewed_notifications(user)

        print('farm metadata ', farm.farm_metadata.programmed_farmsize)
        return render(request, self.template_name, {"idadinotification": not_viewed, "farmwithid": json.dumps([{"name": "Farm", "id": farm.id}]), 
                                                    "totalsize": farm.farm_metadata.programmed_farmsize, 
                                                    "idadi": 1, 
                                                    "farmer": farm.farm_metadata.owner,
                                                    "profile":farm.farm_metadata.owner.photo.url,
                                                    "usergroup": user_group, "fname": name,
                                                    "farmId": farm.id,
                                                    "record_id": farm.farm_metadata.id,
                                                    "gatherman": gatherman,
                                                    "metadata": [{"name": "Farm", "id": farm.id}],
                                                    "lname": lname, "photo": photo})

farm_info = ViewFarmInfo.as_view()


class ViewFarmersInfo(View):
    template_name = 'administrator/viewfarmerinfo.html'

    @method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        owner = self.kwargs.get('fid', None)
        farmer = Owner.objects.get(id=int(owner))
        farms = []
        farmsMetadata = []
        farmsWithFarmId = []
        totalsize = 0
        mt_id = 1
        print('farms ', farms)
        sizes = []
        for farm in Farm.objects.all():
            if farm.farm_metadata.owner.nationalID == farmer.nationalID:
                farms.append(farm)
                sizes.append(farm.farm_metadata.coordinates.id)


        fm_size_elements = []
        for fm in farms:
            totalsize += float(fm.pragrammed_farmsize)
            fm_size_elements.append(fm.pragrammed_farmsize)
            obj = {"name": f"Farm {mt_id}", "farm": fm}
            fIdObj = {"name": f"Farm {mt_id}", "id": fm.id}
            mt_id += 1
            farmsWithFarmId.append(fIdObj)
            farmsMetadata.append(obj)
        profile = farmer.photo.url
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        lname = ""
        not_viewed = not_viewed_notifications(user)
        user_group = "admin"
        print('gatherman ', gatherman)
        return render(request, self.template_name, {"idadinotification":not_viewed, "farmwithid": json.dumps(farmsWithFarmId), "metadata": farmsMetadata, "totalsize": totalsize, "farms": farms, "idadi": len(farms), "farmer": farmer, 
                                                    "profile": profile, "gatherman": gatherman, "usergroup": user_group, "fname": name,
                                                    "lname": lname, "photo": photo})


view_farmer_info = ViewFarmersInfo.as_view()

# when you delete the gathered info the farm will be deleted on CASCADE


class DeleteGatheredInfo(View):
    @method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        info_id = self.kwargs.get('rid', None)

        info = GatheredInfo.objects.get(id=int(info_id))

        info.delete()
        return HttpResponseRedirect(reverse('farms'))


delete_info = DeleteGatheredInfo.as_view()


class GatherProfileView(View):
    template_name = 'administrator/user/viewgatherinfoorprofile.html'

    @method_decorator(permission_required('mkulima.view_gatherprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        gatherman = GatherProfile.objects.get(id=int(self.kwargs.get('gid')))
        user = self.request.user
        not_viewed = 0
        if hasattr(user, 'adminprofile'):
            admin = user.adminprofile
            photo = admin.photo.url
            name = admin.name
            lname = ""
            user_group = "admin"
            not_viewed = not_viewed_notifications(user)

        elif hasattr(user, 'gather'):
            mtaalamu = user.gather
            photo = mtaalamu.profile_picture.url
            name = mtaalamu.first_name
            lname = mtaalamu.last_name
            user_group = "Gatherman"

        infos = GatheredInfo.objects.filter(gathered_by=gatherman).count()
        # report_by_argo = reports.filter(argonomist=argonomist).count()
        # records = GatheredInfo.
        # gatherprofilephoto ndo profile ya gather ya kuangalia
        # info ni idadi ya info alizo-add...
        return render(request, self.template_name, {"idadinotification": not_viewed, "infos": infos, "gatherman": gatherman, "profilephoto": gatherman.profile_picture.url, "usergroup": user_group, "fname": name,
                                                    "lname": lname, "photo": photo})


view_gatherprofile = GatherProfileView.as_view()


class ProfileArgoView(View):
    template_name = 'administrator/user/viewargoinfoorprofile.html'

    @ method_decorator(permission_required('mkulima.view_argonprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        argonomist = ArgonProfile.objects.get(id=int(self.kwargs.get('aid')))
        user = self.request.user
        not_viewed = 0
        if hasattr(user, 'adminprofile'):
            admin = user.adminprofile
            photo = admin.photo.url
            name = admin.name
            lname = ""
            user_group = "admin"
            not_viewed = not_viewed_notifications(user)

        elif hasattr(user, 'argonomic'):
            mtaalamu = user.argonomic
            photo = mtaalamu.profile_picture.url
            name = mtaalamu.first_name
            lname = mtaalamu.last_name
            user_group = "Argonomist"

        reports = ArgoReport.objects.filter(is_completed_and_recommended=True)
        report_by_argo = reports.filter(argonomist=argonomist).count()

        return render(request, self.template_name, {"idadinotification": not_viewed, "reports": report_by_argo, "argonomist": argonomist, "profilephoto": argonomist.profile_picture.url, "usergroup": user_group, "fname": name,
                                                    "lname": lname, "photo": photo})


view_profile = ProfileArgoView.as_view()


class DeleteArgoReport(View):
    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        report_id = self.kwargs.get("rid", None)
        report = ArgoReport.objects.get(id=int(report_id))

        report.delete()
        return HttpResponseRedirect(reverse("testandrecomms"))


drop_report = DeleteArgoReport.as_view()


class ViewGather(View):
    template_name = "administrator/user/viewgather.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        pro_id = self.kwargs.get('gid', None)
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        not_viewed = not_viewed_notifications(user)
        
        if (pro_id):
            profile = GatherProfile.objects.get(id=int(pro_id))

            return render(request, self.template_name, {"idadinotification": not_viewed, "gatherman": profile, "fname": name, "photo": photo})

    def post(self, request, *args, **kwargs):
        pro_id = self.kwargs.get('gid', None)
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name

        if (pro_id):
            gatherman = GatherProfile.objects.get(id=int(pro_id))
        try:
            fname = request.POST.get('fname', None)
            lname = request.POST.get('lname', None)
            phone = request.POST.get('phone', None)
            country = request.POST.get('country', None)
            region = request.POST.get('region', None)
            district = request.POST.get('district', None)
            ward = request.POST.get('ward', None)
            profile = request.FILES.get('profilepicture', None)
            isactive = request.POST.get('isactive', None)
            # print({
            #     "first": fname,
            #     "last": lname,
            #     "phone": phone,
            #     "country": country,
            #     "district": district,
            #     "ward": ward,
            #     "profile": profile,
            #     "isactive": isactive
            # })

            if isactive == 'on':
                isactive = True
            else:
                isactive = False

            print('The user status to add its role ', isactive, type(isactive))

            gatherman.first_name = fname
            gatherman.last_name = lname
            gatherman.phone = phone
            gatherman.country = country
            gatherman.region = region
            gatherman.district = district
            gatherman.ward = ward

            if (profile):
                gatherman.profile_picture = File(profile)

            gatherman.save()
            gatherman.user.is_active = isactive
            gatherman.user.save()

            return HttpResponseRedirect(reverse('usergatherman'))
        except Exception as err:
            print('ERROR OCCURRED ', err)
            return render(request, self.template_name, {"gatherman": gatherman, "fname": name, "photo": photo})


view_gather = ViewGather.as_view()


class AdminDeleteGather(View):
    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        pro_id = self.kwargs.get('pid', None)

        print('This is profile id of gather ', pro_id)

        if pro_id:
            profile = GatherProfile.objects.get(id=int(pro_id))
            # profile.delete()
            # you should delete the user and not the profile
            profile.user.delete()
            return HttpResponseRedirect(reverse("usergatherman"))


ad_del_gather = AdminDeleteGather.as_view()


class AdminDeleteArgonomist(View):
    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        pro_id = self.kwargs.get('pid', None)
        print('I received the profile_id ', pro_id)
        if pro_id:
            profile = ArgonProfile.objects.get(id=int(pro_id))
            # you should delete user and not the profile..
            profile.user.delete()
            # profile.delete()
            return HttpResponseRedirect(reverse("userargonomist"))


ad_del_argo = AdminDeleteArgonomist.as_view()


class ViewArgonomist(View):
    template_name = "administrator/user/viewargo.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        pro_id = self.kwargs.get('gid', None)
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        not_viewed = not_viewed_notifications(user)
        if (pro_id):
            profile = ArgonProfile.objects.get(id=int(pro_id))

            return render(request, self.template_name, {"idadinotification": not_viewed, "argonomic": profile, "fname": name, "photo": photo})

    def post(self, request, *args, **kwargs):
        pro_id = self.kwargs.get('gid', None)
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name

        if (pro_id):
            argonomist = ArgonProfile.objects.get(id=int(pro_id))
        try:
            fname = request.POST.get('fname', None)
            lname = request.POST.get('lname', None)
            phone = request.POST.get('phone', None)
            country = request.POST.get('country', None)
            region = request.POST.get('region', None)
            district = request.POST.get('district', None)
            ward = request.POST.get('ward', None)
            profile = request.FILES.get('profilepicture', None)
            isactive = request.POST.get('isactive', None)

            if isactive == 'on':
                isactive = True
            else:
                isactive = False

            print('The user status to add its role ', isactive, type(isactive))

            argonomist.first_name = fname
            argonomist.last_name = lname
            argonomist.phone = phone
            argonomist.country = country
            argonomist.region = region
            argonomist.district = district
            argonomist.ward = ward

            if (profile):
                argonomist.profile_picture = File(profile)

            argonomist.save()
            argonomist.user.is_active = isactive
            argonomist.user.save()

            return HttpResponseRedirect(reverse('userargonomist'))
        except Exception as err:
            print('ERROR OCCURRED ', err)
            return render(request, self.template_name, {"argonomic": argonomist, "fname": name, "photo": photo})


view_argo = ViewArgonomist.as_view()


class TestsRecommendations(View):
    template_name = "administrator/testsandrecommends.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        not_viewed = not_viewed_notifications(user)
        reports = ArgoReport.objects.all()

        return render(request, self.template_name, {"idadinotification": not_viewed, "reports": reports, "fname": name, "photo": photo})

    def post(self, request):
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        reports = ArgoReport.objects.all()

        ids = request.POST.get('profileids', None)
        parsed_ids = json.loads(ids)

        if (len(parsed_ids) > 0):
            for id in parsed_ids:
                report = ArgoReport.objects.get(id=int(id))
                report.delete()

        return render(request, self.template_name, {"reports": reports, "fname": name, "photo": photo})


testsrecoms = TestsRecommendations.as_view()


class CropsReport(View):
    template_name = "administrator/reports/crops.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        not_viewed = not_viewed_notifications(user)
        total_recommended = 0
        not_recommended = 0
        for farm in Farm.objects.all():
            try:
                if farm.report.all().last().is_completed_and_recommended:
                    total_recommended += 1
                else:
                    not_recommended += 1
            except Exception as err:
                # some farms which is not yet touched/test/recomms have no any report will return the error here when u try
                # to access .is_completed_and_recommended. for these catch error and increment is not_recommended
                # that's different from JS which when key is not found it return 'Undefine' and not throwing error like in py.
                not_recommended += 1

        farm_metadata = {
            "recommended": total_recommended,
            "not_recommended": not_recommended,
            "total": Farm.objects.all().count(),
            "recom_percent": str(round((round(total_recommended/Farm.objects.all().count(), 2) * 100))) + '%',
            "not_recom_percent": str(100 - round((round(total_recommended/Farm.objects.all().count(), 2) * 100))) + '%'
        }

        print(farm_metadata)

        return render(request, self.template_name, {"idadinotification": not_viewed, "farm_metadata": farm_metadata, "fname": name, "photo": photo})


crops = CropsReport.as_view()


class SoilTestResultReport(View):
    template_name = "administrator/reports/soilreport.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        not_viewed = not_viewed_notifications(user)
        reports = ArgoReport.objects.filter(is_completed_and_recommended=True)
        return render(request, self.template_name, {"idadinotification": not_viewed, "reports": reports, "idadi": reports.count(), "fname": name, "photo": photo})


test_results = SoilTestResultReport.as_view()


class RecommendedCultivation(View):
    template_name = "administrator/reports/cultivation.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        not_viewed = not_viewed_notifications(user)
        reports = ArgoReport.objects.filter(is_completed_and_recommended=True)
        return render(request, self.template_name, {"idadinotification": not_viewed, "reports": reports, "idadi": reports.count(), "fname": name, "photo": photo})


cultivation = RecommendedCultivation.as_view()


class FarmRecommendedSeedAmount(View):
    template_name = "administrator/reports/recommendedseed.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        not_viewed = not_viewed_notifications(user)
        reports = ArgoReport.objects.filter(is_completed_and_recommended=True)
        return render(request, self.template_name, {"idadinotification": not_viewed, "reports": reports, "idadi": reports.count(), "fname": name, "photo": photo})


seed_amount = FarmRecommendedSeedAmount.as_view()


class FarmRecommendedCrops(View):
    template_name = "administrator/reports/recommendedcrops.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        not_viewed = not_viewed_notifications(user)
        reports = ArgoReport.objects.filter(is_completed_and_recommended=True)
        return render(request, self.template_name, {"idadinotification": not_viewed ,"reports": reports, "idadi": reports.count(), "fname": name, "photo": photo})


recommended_crops = FarmRecommendedCrops.as_view()


class EstimatedYieldReport(View):
    template_name = "administrator/reports/yield.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        not_viewed = not_viewed_notifications(user)
        reports = ArgoReport.objects.filter(is_completed_and_recommended=True)
        return render(request, self.template_name, {"idadinotification": not_viewed, "reports": reports, "idadi": reports.count(), "fname": name, "photo": photo})


yield_report = EstimatedYieldReport.as_view()


class RecommendedFertilizersReport(View):
    template_name = "administrator/reports/fertilizers.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        not_viewed = not_viewed_notifications(user)
        reports = ArgoReport.objects.filter(is_completed_and_recommended=True)

        return render(request, self.template_name, {"idadinotification": not_viewed, "reports": reports, "idadi": reports.count(), "fname": name, "photo": photo})


fertilizer_report = RecommendedFertilizersReport.as_view()


class FarmersReport(View):
    template_name = "administrator/reports/farmers.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        not_viewed = not_viewed_notifications(user)
        farms = Farm.objects.all()
        return render(request, self.template_name, {"idadinotification": not_viewed, "farms": farms, "idadi": farms.count(), "fname": name, "photo": photo})


farmer_report = FarmersReport.as_view()


class FarmReportView(View):
    template_name = "administrator/reports/farms.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        not_viewed = not_viewed_notifications(user)

        farms = Farm.objects.all()
        return render(request, self.template_name, {"idadinotification": not_viewed, "farms": farms, "idadi": farms.count(), "fname": name, "photo": photo})


farms_report = FarmReportView.as_view()


class FarmsView(View):
    template_name = "administrator/information/farms.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        not_viewed = not_viewed_notifications(user)

        farms = Farm.objects.all()
        return render(request, self.template_name, {"idadinotification": not_viewed, "farms": farms, "idadi": farms.count(), "fname": name, "photo": photo})

    def post(self, request):
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        farms = Farm.objects.all()

        ids = request.POST.get('profileids', None)
        print('Needs to be deleted ', ids)
        parsed_ids = json.loads(ids)

        if (len(parsed_ids) > 0):
            for id in parsed_ids:
                farm = Farm.objects.get(id=int(id))
                farm.delete()

        return render(request, self.template_name, {"farms": farms, "idadi": farms.count(), "fname": name, "photo": photo})


farms = FarmsView.as_view()


class FilterGatherByYear(View):
    template_name = "administrator/user/gatherman.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        year = request.GET.get('year', None)

        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name

        output_gathermen = []
        try:
            if int(year):
                for gatherman in GatherProfile.objects.all():
                    # kama ka-ass year which is not string hapa itagoma..
                    if gatherman.user.joined.year == int(year):
                        output_gathermen.append(gatherman)

            return render(request, self.template_name, {"month": "all", "status": "all", "year": year, "idadi": len(output_gathermen), "gathermen": reversed(output_gathermen), "fname": name, "photo": photo})

        except Exception as err:
            print('err ', err)
            return HttpResponseRedirect(reverse('userargonomist'))


gather_by_year = FilterGatherByYear.as_view()


class FilterGatherByMonth(View):
    template_name = "administrator/user/gatherman.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        month = request.GET.get('month', None)
        print('month ', month, type(month))
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        output_gathers = []

        try:
            if int(month):
                for gatherman in GatherProfile.objects.all():
                    # kama ka-ass year which is not string hapa itagoma..
                    if gatherman.user.joined.month == int(month):
                        output_gathers.append(gatherman)

            return render(request, self.template_name, {"status": "all", "month": month, "idadi": len(output_gathers), "gathermen": reversed(output_gathers), "fname": name, "photo": photo})

        except Exception as err:
            print('err ', err)
            return HttpResponseRedirect(reverse('userargonomist'))


class FilterGatherByStatus(View):
    template_name = "administrator/user/gatherman.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        status = request.GET.get('status', 'all')

        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name

        # get all user who is argonomist, i can do this by querying the argonomist model
        gathermen = GatherProfile.objects.all()
        active_gathermen = []
        inactive_gathermen = []

        if status == 'alive':
            for gather in gathermen:
                if gather.user.is_active:
                    active_gathermen.append(gather)

            return render(request, self.template_name, {"month": "all", "status": status, "idadi": len(active_gathermen), "gathermen": reversed(active_gathermen), "fname": name, "photo": photo})

        if status == 'inactive':
            for gather in gathermen:
                if gather.user.is_active == False:
                    inactive_gathermen.append(gather)

            return render(request, self.template_name, {"month": "all", "status": status, "idadi": len(inactive_gathermen), "gathermen": reversed(inactive_gathermen), "fname": name, "photo": photo})

        if status == 'all':
            return render(request, self.template_name, {"month": "all", "status": status, "idadi": len(gathermen), "gathermen": reversed(gathermen), "fname": name, "photo": photo})


gather_status = FilterGatherByStatus.as_view()

gather_month = FilterGatherByMonth.as_view()


class FilterArgonomistByMonth(View):
    template_name = "administrator/user/argonomist.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        month = request.GET.get('month', None)
        print('month ', month, type(month))
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        output_argonomists = []
        try:
            if int(month):
                for argonomist in ArgonProfile.objects.all():
                    # kama ka-ass year which is not string hapa itagoma..
                    if argonomist.user.joined.month == int(month):
                        output_argonomists.append(argonomist)

            return render(request, self.template_name, {"status": "all", "month": month, "idadi": len(output_argonomists), "argonomists": reversed(output_argonomists), "fname": name, "photo": photo})

        except Exception as err:
            print('err ', err)
            return HttpResponseRedirect(reverse('userargonomist'))


month_filter = FilterArgonomistByMonth.as_view()


class FilterArgonomistByYear(View):
    template_name = "administrator/user/argonomist.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        year = request.GET.get('year', None)

        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name

        output_argonomists = []
        try:
            if int(year):
                for argonomist in ArgonProfile.objects.all():
                    # kama ka-ass year which is not string hapa itagoma..
                    if argonomist.user.joined.year == int(year):
                        output_argonomists.append(argonomist)

            return render(request, self.template_name, {"month": "all", "status": "all", "year": year, "idadi": len(output_argonomists), "argonomists": reversed(output_argonomists), "fname": name, "photo": photo})

        except Exception as err:
            print('err ', err)
            return HttpResponseRedirect(reverse('userargonomist'))


year_filter = FilterArgonomistByYear.as_view()


class FilterArgonomistsByStatus(View):
    # for this to work you should send all data to us.. year, months and status
    template_name = "administrator/user/argonomist.html"

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        status = request.GET.get('status', 'all')

        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name

        # get all user who is argonomist, i can do this by querying the argonomist model
        argonomists = ArgonProfile.objects.all()
        active_argonomists = []
        inactive_argonomists = []

        if status == 'alive':
            for argonomist in argonomists:
                # filter for both year and month
                if argonomist.user.is_active:
                    active_argonomists.append(argonomist)

            return render(request, self.template_name, {"month": "all", "status": status, "idadi": len(active_argonomists), "argonomists": reversed(active_argonomists), "fname": name, "photo": photo})

        if status == 'inactive':
            for argonomist in argonomists:
                if argonomist.user.is_active == False:
                    inactive_argonomists.append(argonomist)

            return render(request, self.template_name, {"month": "all", "status": status, "idadi": len(inactive_argonomists), "argonomists": reversed(inactive_argonomists), "fname": name, "photo": photo})

        if status == 'all':
            return render(request, self.template_name, {"month": "all", "status": status, "idadi": len(argonomists), "argonomists": reversed(argonomists), "fname": name, "photo": photo})


argonomist_status = FilterArgonomistsByStatus.as_view()


class GathermanUser(View):
    template_name = 'administrator/user/gatherman.html'

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        gathermen = GatherProfile.objects.filter(profileIsCompleted = True)
        not_viewed = not_viewed_notifications(user)
        return render(request, self.template_name, {"idadinotification": not_viewed, "month": "all", "status": "all", "gathermen": reversed(gathermen), "idadi": len(gathermen), "fname": name, "photo": photo})

    def post(self, request):
        ids = request.POST.get("profileids", None)
        gathermen = GatherProfile.objects.all()
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        print('These profiles need to be deleted ', ids)
        parsed_ids = json.loads(ids)
        if (len(parsed_ids) > 0):
            # we have sth to delete
            for id in parsed_ids:
                user = get_user_model().objects.get(id=int(id))
                # by relation between user and gatherprofile, deleting the user delete th profile
                user.delete()

        return render(request, self.template_name, {"month": "all", "status": "all", "gathermen": gathermen, "fname": name, "photo": photo})


gatherman = GathermanUser.as_view()


class ArgonomistUser(View):
    template_name = 'administrator/user/argonomist.html'

    @ method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        not_viewed_noti = not_viewed_notifications(user)
        argonomists = ArgonProfile.objects.filter(profileIsCompleted=True)

        return render(request, self.template_name, {"idadinotification": not_viewed_noti,"month": "all", "idadi": len(argonomists), "status": "all", "argonomists": reversed(argonomists), "fname": name, "photo": photo})

    def post(self, request):
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        argonomists = ArgonProfile.objects.all()

        ids = request.POST.get("profileids", None)
        parsed_ids = json.loads(ids)
        if (len(parsed_ids) > 0):
            for id in parsed_ids:
                user = get_user_model().objects.get(id=int(id))
                user.delete()

        return render(request, self.template_name, {"month": "all", "status": "all", "argonomists": reversed(argonomists), "fname": name, "photo": photo})


argonomist = ArgonomistUser.as_view()


class HomeView(View):
    template_name = 'administrator/index.html'

    @method_decorator(permission_required('mkulima.view_adminprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        user = self.request.user
        admin = user.adminprofile
        photo = admin.photo.url
        name = admin.name
        farms = Farm.objects.all()

        notifications = notificationsByUser(user.id)
        notification_length = 0
        # only show the number of notification which is not viewed yet..
        for notification in notifications:
            if notification.isViewed:
                continue
            notification_length += 1

        
        # argoreport is accessed farms and tested and recommended so lets load all reports which is already tested and recommened
        reports = ArgoReport.objects.filter(is_completed_and_recommended=True).reverse()
        total_reports = len(list(reports))
        print('reports ', reports.first().added_on, reports.first().id, reports.last().added_on, reports.last().id)
        latest = []
        for report in reports:
            index = list(reports).index(report)
            if index < 5:
                latest.append(report)
        reports = latest
        activeargos = []
        for argonomist in ArgonProfile.objects.all():
            if argonomist.user.is_active:
                activeargos.append(argonomist)

        activegathers = []

        for gatherman in GatherProfile.objects.all():
            if gatherman.user.is_active:
                activegathers.append(gatherman)

        return render(request, self.template_name, { "notifications": notifications, "idadinotification": notification_length, "reports": reports, "reportIdadi": total_reports, "agathers": len(activegathers), "aargos": len(activeargos), "farms": len(farms), "fname": name, "photo": photo})


home_view = HomeView.as_view()
