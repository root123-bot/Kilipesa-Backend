from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from MkulimaBackend.mkulima.models import *
from django.core.files import File
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
import datetime as dt
# behind the scene pytz we're using also use datetime... so to avoid confusion you should have ur
# imported datetime in given alia
import pytz
import sys
from django.shortcuts import resolve_url
from django.contrib.auth.models import Group
from .forms import ChangePassword
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

tztimezone = pytz.timezone("Africa/Dar_es_Salaam")


class FetchArgonomistAPI(APIView):
    def post(self, request, *args, **kwargs):
        argo_id = request.data['id']
        argonomist = ArgonProfile.objects.get(id=int(argo_id))

        serializer = ArgonomistSerializer(argonomist)

        # return response of status code 200
        return Response(serializer.data, status=status.HTTP_200_OK)


argonomist_details = FetchArgonomistAPI.as_view()


class EditTestsRecommendation(View):
    template_name = "argonomist/editt&recom.html"

    @method_decorator(permission_required('mkulima.view_argonprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        report_id = self.kwargs.get("rid", None)
        user = self.request.user

        # this should be accessed by both admin and argonomist
        if hasattr(user, "adminprofile"):
            admin = user.adminprofile
            photo = admin.photo.url
            name = admin.name
            lname = ""
            user_group = "admin"

            # hatuihitaji hii argonomist_id kwa admin..
            argonomist_id = None

        else:
            argonomist = self.request.user.argonomic
            photo = argonomist.profile_picture.url
            name = argonomist.first_name
            lname = argonomist.last_name
            user_group = "Argonomist"
            argonomist_id = argonomist.id
        if report_id:
            report = ArgoReport.objects.get(id=int(report_id))

            info = report.farm.farm_metadata
            return render(request, self.template_name, {"argonomist": argonomist_id, "usergroup": user_group, "infoid": info.id, "report": report, "fname": name,
                                                        "lname": lname, "photo": photo})


edit_report = EditTestsRecommendation.as_view()


class ChangePassword(View):
    template_name = 'argonomist/changepassword.html'

    @method_decorator(permission_required('mkulima.view_argonprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        argonomist = self.request.user.argonomic

        return render(request, self.template_name, {"argonomic": argonomist, "fname": self.request.user.argonomic.first_name, "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})

    def post(self, request):

        argonomist = self.request.user.argonomic

        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user = self.request.user
        print(request.POST.get('password'), request.POST.get(
            'password1'), request.POST.get('password2'))
        if (password1 != password2):
            return render(request, self.template_name, {"message": "confirmed password is not the same to new password", "argonomic": argonomist, "fname": self.request.user.argonomic.first_name, "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})

        if (len(password1.strip()) < 6):
            return render(request, self.template_name, {"message": "Use longer password more than 6 characters is required", "argonomic": argonomist, "fname": self.request.user.argonomic.first_name, "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})

        if user.check_password(password):
            # that means the password exist let's change it..
            user.password = make_password(password1)
            user.save()
            # return render(request, self.template_name, {"argonomic": argonomist, "fname": self.request.user.argonomic.first_name, "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})
            # once una-vyochange password basi eti user anakuwa hatambuliki, nishajua sababu ni kwa sababu user
            # anae-exist ni yule aliye-login na password ya mwanzo ko hapa anakuwa hatambuliki tena cha kufanya inabid
            # um-log in huyo user ndo uliyempa password mpya ndo itakubali...
            login(request, user)
            return HttpResponseRedirect(reverse("argo_full_profile"))

        return render(request, self.template_name, {"argonomist": argonomist.id, "message": "Error in changing password", "argonomic": argonomist, "fname": self.request.user.argonomic.first_name, "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})


change_password = ChangePassword.as_view()


class EditProfile(View):
    template_name = 'argonomist/edit_profile.html'

    @method_decorator(permission_required('mkulima.view_argonprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        argonomist = self.request.user.argonomic
        # print(argonomist.id, ' argonomist')
        return render(request, self.template_name, {"argonomic": argonomist, "fname": self.request.user.argonomic.first_name, "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})

    def post(self, request):
        argonomist = self.request.user.argonomic
        try:
            fname = request.POST.get('fname', None)
            lname = request.POST.get('lname', None)
            phone = request.POST.get('phone', None)
            country = request.POST.get('country', None)
            region = request.POST.get('region', None)
            district = request.POST.get('district', None)
            ward = request.POST.get('ward', None)
            profile = request.FILES.get('profilepicture', None)

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
            return HttpResponseRedirect(reverse('argo_full_profile'))
        except Exception as err:
            print('something went wrong ', err)
            return render(request, self.template_name, {"argonomic": argonomist, "fname": self.request.user.argonomic.first_name, "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})


edit_profile = EditProfile.as_view()


class RecommendView(View):
    template_name = 'argonomist/recommend.html'

    @method_decorator(permission_required('mkulima.view_argonprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        report_id = self.kwargs.get('rid')
        report = ArgoReport.objects.get(id=report_id)
        user = self.request.user
        if hasattr(user, 'adminprofile'):
            admin = user.adminprofile
            photo = admin.photo.url
            name = admin.name
            lname = ""
            user_group = "admin"
            # sio muhimu hapa coz naihitaji hii kwa argonomist ku-reference his profile_id
            argonomist_id = None
        else:

            if report.argonomist.id != self.request.user.argonomic.id:
                # you can't recommend the report you don't own...
                return HttpResponseRedirect(reverse('argontasks'))

            argonomist = report.argonomist
            photo = argonomist.profile_picture.url
            name = argonomist.first_name
            lname = argonomist.last_name
            user_group = "Argonomist"
            argonomist_id = argonomist.id
        return render(request, self.template_name, {"argonomist": argonomist_id, "usergroup": user_group, "farmsize": report.farm.size, "infoid": report.farm.farm_metadata.id, "report": report, "fname": name,
                                                    "lname": lname, "photo": photo})

    def post(self, request, *args, **kwargs):
        report_id = self.kwargs.get('rid')
        try:
            try:
                crop = request.POST.get('crop', None)
                fertilizer = request.POST.get('fertilizer', None)
                seed = request.POST.get('seed', None)
                culttype = request.POST.get('culttype', None)
                output = request.POST.get('output', None)
                fweight = request.POST.get('fweight', None)

                recommendations = Recommendations.objects.create(
                    crop=crop,
                    fertilizer_name=fertilizer,
                    amount_of_fertilizer=fweight,
                    seed_amonunt_per_size_of_farm_or_hectare=seed,
                    cultivation_type=culttype,
                    standard_yield=output,
                )

                recommendations.save()
            except Exception as err:
                print('eror occurred in saving the recommendation ', err)

            # then i saved and having the recommend instance i need to link it to argoreport
            report = ArgoReport.objects.get(id=report_id)

            user = self.request.user
            if hasattr(user, 'adminprofile'):
                report.recommendation = recommendations
                report.is_completed_and_recommended = True
                report.save()
                return HttpResponseRedirect(reverse('testandrecomms'))

            else:
                if report.argonomist.id != self.request.user.argonomic.id:
                    return HttpResponseRedirect(reverse('argontasks'))

                # lets save it to our report and we should mark it complete..
                report.recommendation = recommendations
                report.is_completed_and_recommended = True
                report.save()
                return HttpResponseRedirect(reverse('argo_full_profile'))
        except Exception as err:
            print('Big error have been occurred which is ', err)
            return render(request, self.template_name, {"infoid": report.farm.farm_metadata.id, "report": report, "fname": self.request.user.argonomic.first_name, })


recommend = RecommendView.as_view()


class EditTest(View):
    template_name = 'argonomist/edittest.html'

    # this permission of view_argonomist is valid to use in most of case if we want only argonomist to pass the test.
    @method_decorator(permission_required('mkulima.view_argonprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        report_id = self.kwargs.get('rid')
        report = ArgoReport.objects.get(id=int(report_id))
        info = report.farm.farm_metadata
        user = self.request.user
        if hasattr(user, 'adminprofile'):
            admin = user.adminprofile
            photo = admin.photo.url
            name = admin.name
            lname = ""
            user_group = "admin"
            argonomist_id = None
        else:

            if (report.argonomist.id != self.request.user.argonomic.id):
                return HttpResponseRedirect(reverse('argo_full_profile'))

            argonomist = report.argonomist
            photo = argonomist.profile_picture.url
            name = argonomist.first_name
            lname = argonomist.last_name
            user_group = "Argonomist"
            argonomist_id = argonomist.id
        return render(request, self.template_name, {
            "usergroup": user_group,
            "task": info,
            "report": report,
            "fname": name,
            "lname": lname,
            "photo": photo,
            "argonomist": argonomist_id,
        })

    def post(self, request, *args, **kwargs):
        report_id = self.kwargs.get('rid')
        report = ArgoReport.objects.get(id=int(report_id))

        report = ArgoReport.objects.get(id=int(report_id))
        info = report.farm.farm_metadata
        user = self.request.user
        if hasattr(user, 'adminprofile'):
            pass
        else:
            argonomist = self.request.user.argonomic
            report_argonomist = report.argonomist
            if (report_argonomist.id != argonomist.id):
                return HttpResponseRedirect(reverse('argo_full_profile'))

        color = request.POST.get('scolor', None)
        structure = request.POST.get('sstructure', None)
        form = request.POST.get('sform', None)
        texture = request.POST.get('stexture', None)
        density = request.POST.get('sdensity', None)
        porosity = request.POST.get('sporosity', None)
        moisture = request.POST.get('smoisture', None)
        temperature = request.POST.get('stemp', None)
        phosphorus = request.POST.get('sphos', None)
        potassium = request.POST.get('spota', None)
        nitrogen = request.POST.get('snitr', None)
        organic = request.POST.get('sorganic', None)
        pH = request.POST.get('sph', None)

        if (color and structure and form and texture and density
            and porosity and moisture and temperature and phosphorus
                and potassium and nitrogen and organic and pH):

            tresult = report.test_results

            tresult.soil_color = color
            tresult.soil_structure = structure
            tresult.soil_form = form
            tresult.soil_texture = texture
            tresult.bulk_density = density
            tresult.soil_porosity = porosity
            tresult.soil_moisture = moisture
            tresult.soil_temperature = temperature
            tresult.phosphorus_level = phosphorus
            tresult.potassium_level = potassium
            tresult.nitrogen_level = nitrogen
            tresult.organic_matter = organic
            tresult.soil_ph = pH

            tresult.save()

            # redirect to recommendation...
            if hasattr(user, 'adminprofile'):
                return HttpResponseRedirect(resolve_url("recommend", rid=report.id))

            return HttpResponseRedirect(resolve_url("filltest", rid=info.id))


edit_test = EditTest.as_view()


class FillTest(View):
    template_name = 'argonomist/testmetadata.html'

    @method_decorator(permission_required('mkulima.view_argonprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # make sure the guy is assigned the task
    def get(self, request, *args, **kwargs):
        task_id = self.kwargs.get('rid')
        info = GatheredInfo.objects.get(id=int(task_id))
        # check if there is report of this info you should
        # redirect to recommend page.. so info.farm
        assignedto = info.assignedTo
        # then you should check if the user is in assigned to
        user = self.request.user
        argonomist = user.argonomic
        if assignedto.id != argonomist.id:
            # its not your info/farm
            return render(request, self.template_name, {"task": info, "fname": self.request.user.argonomic.first_name,
                                                        "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})

        print(assignedto, ' assignedto')
        # check if there is report of this farm..
        farm = info.gatheredinfo
        print('farm ', farm, farm.report.all())
        # check if there is a report belong to this farm..
        reports = farm.report.all()
        print('reports ', reports)
        # theck if there is report of this 'gathered info' and make sure
        #
        # is there is report for this gathered info
        # if there are reports length > 1 then you should check if the
        # but what if we have more than 1 report of given shamba, then we
        # should maybe depend on gathered info id coz here id is unique
        # but 'for given' infogathered we can have the
        # for this we have only one GatheredInfo since Farm and GatheredInfo is
        # onetoone relationship..
        if len(reports) > 0:
            print('greater than 1')
            # lets go to the latest report and from that latest we should check
            # if that info.. after getting latest we should check if that report
            # belong to this profile/argonomist..
            # can we have many reports for that gathered info.. we should check the
            # latest one.. japo sijui kama kuna scenario tunaweza tukawa na reports
            # nyingi which is not completed... sizani lakini.. ko hapa inabidi tu-assume
            # tunayo moja tu
            rep = reports[len(reports) - 1]
            # from that lets check if that report is_completed or not
            # if its completed then check if is_completed_and_recommended

            if rep.is_completed:
                if rep.is_completed_and_recommended:
                    print('is already recommended')
                    # no need to edit or add the recommendation its already locked
                    return HttpResponseRedirect(reverse('argo_full_profile'))

                else:
                    # allow to add recommendatio
                    return HttpResponseRedirect(resolve_url('recommend', rid=rep.id))

            else:
                print(
                    'we are in else statement, so every report by default it have iscomplete true...')
                # and remember everytime we create a report we mark is_complete=True means there is no any report created for that data which is 'impossible' since we loaded report then there is no report it does not make sense.
                return HttpResponseRedirect(resolve_url('argontasks'))

        return render(request, self.template_name, {"task": info, "fname": self.request.user.argonomic.first_name,
                                                    "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})

    def post(self, request, *args, **kwargs):
        task_id = self.kwargs.get('rid')
        info = GatheredInfo.objects.get(id=int(task_id))
        user = self.request.user
        argonomist = user.argonomic
        farm = info.gatheredinfo
        color = request.POST.get('scolor', None)
        structure = request.POST.get('sstructure', None)
        form = request.POST.get('sform', None)
        texture = request.POST.get('stexture', None)
        density = request.POST.get('sdensity', None)
        porosity = request.POST.get('sporosity', None)
        moisture = request.POST.get('smoisture', None)
        temperature = request.POST.get('stemp', None)
        phosphorus = request.POST.get('sphos', None)
        potassium = request.POST.get('spota', None)
        nitrogen = request.POST.get('snitr', None)
        organic = request.POST.get('sorganic', None)
        pH = request.POST.get('sph', None)

        dropdown = "Open this select menu"

        if ((color != dropdown) and (structure != dropdown) and (form != dropdown) and (texture != dropdown) and density
                and porosity and moisture and temperature and phosphorus and potassium and nitrogen and organic and pH):
            print('Everything is good!')

            # lets round, uzuri wa .round() ni kwamba yenyewe if its decimal it round to given decimal place if its integer it l
            # leave it as integer for exampel >> a = 10.. round(a, 2) =>> 10; a = 10.989932 .. round(a, 2) =>> 10.99
            # to convert number in float in python use.. float() but it return in 1 decimal place for example
            # a = 10, float(a) =>> 10; a=10.238; float(a) =>> 10.238

            try:
                result = TestResult.objects.create(
                    sample_id=task_id,
                    soil_color=color,
                    soil_temperature=temperature,
                    soil_structure=structure,
                    soil_texture=texture,
                    soil_porosity=porosity,
                    soil_ph=pH,
                    soil_form=form,
                    bulk_density=density,
                    soil_moisture=moisture,
                    phosphorus_level=phosphorus,
                    potassium_level=potassium,
                    nitrogen_level=nitrogen,
                    organic_matter=organic,
                )

                result.save()

                report = ArgoReport.objects.create(
                    argonomist=argonomist,
                    sampleId=task_id,
                    test_results=result,
                    farm=farm,
                    added_on=dt.datetime.now(tztimezone),
                    is_completed=True
                )
                report.save()
                print('I need to redirect him')
                return HttpResponseRedirect(resolve_url('recommend', rid=report.id))

            except Exception as err:
                print('Some fields is empty ', {
                    "color": color,
                    "structure": structure,
                    "form": form,
                    "texture": texture,
                    "density": density,
                    "porosity": porosity,
                    "moisture": moisture,
                    "temperature": temperature,
                    "phosphorus": phosphorus,
                    "potassium": potassium,
                    "nitrogen": nitrogen,
                    "organic": organic,
                    "pH": pH
                })
                print('error occured ', err)
                return render(request, self.template_name, {"message": err, "task": info, "fname": self.request.user.argonomic.first_name,
                                                            "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})

            # print(porosity, density, moisture,
            #       temperature, phosphorus, potassium,
            #       nitrogen, organic, pH)

        else:
            print('Some fields is empty ', {
                "color": color,
                "structure": structure,
                "form": form,
                "texture": texture,
                "density": density,
                "porosity": porosity,
                "moisture": moisture,
                "temperature": temperature,
                "phosphorus": phosphorus,
                "potassium": potassium,
                "nitrogen": nitrogen,
                "organic": organic,
                "pH": pH
            })

        return render(request, self.template_name, {"task": info, "fname": self.request.user.argonomic.first_name,
                                                    "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})


fill_test = FillTest.as_view()


class GiveMeTask(View):
    template_name = 'argonomist/testrecord.html'

    @method_decorator(permission_required('mkulima.view_argonprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        info_id = self.kwargs.get('rid')
        info = GatheredInfo.objects.get(id=int(info_id))
        gatheredinfos = GatheredInfo.objects.all()
        owner = info.owner
        coors = info.coordinates

        user = self.request.user
        argonomist = user.argonomic

        if (info.isAssigned):

            assigned_to = info.assignedTo
            if (assigned_to.id != argonomist.id):
                message = "Task have been assigned to other, pick another one"
                return render(request, self.template_name, {"argonomist": argonomist.id, "owner": owner, "message": message, "farm": info.gatheredinfo, "coords": json.loads(coors.allCoords), "infolen": gatheredinfos.count(), "id": info_id, "fname": self.request.user.argonomic.first_name, "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})

            return render(request, self.template_name, {"argonomist": argonomist.id, "isAssigned": True, "owner": owner, "farm": info.gatheredinfo, "coords": json.loads(coors.allCoords), "infolen": gatheredinfos.count(), "id": info_id, "fname": self.request.user.argonomic.first_name, "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})

        else:
            info.assignedTo = argonomist
            info.assigned_at = dt.datetime.now(tztimezone)
            info.isAssigned = True
            info.release_date = dt.datetime.now(
                tztimezone) + dt.timedelta(days=5)
            info.save()
            return HttpResponseRedirect(reverse('argontasks'))


assignTaskToMe = GiveMeTask.as_view()


class CompletedTaskToday(View):
    template_name = "argonomist/completedtoday.html"

    @method_decorator(permission_required('mkulima.view_argonprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        argonomist = self.request.user.argonomic
        reports = argonomist.argoreport.all()
        ainfos = GatheredInfo.objects.filter(assignedTo=argonomist)
        completedTaskReports = []  # these are just a reports
        completedTask = 0

        for info in ainfos:
            farm = info.gatheredinfo
            report = farm.report.all()
            if len(report) > 0:
                print('now im here')
                print(report[len(report) - 1].is_completed_and_recommended)
                if report[len(report) - 1].is_completed_and_recommended == True:
                    # completedTaskReports.append(report[len(report) - 1])
                    completedTask += 1

        noreporttask = 0
        # i don't know why i'm having 2 for loops here
        for info in ainfos:
            farm = info.gatheredinfo
            report = farm.report.all()
            if (len(report) < 1):
                noreporttask += 1
        if len(reports) < 1:
            # idadi ya task/report ni zero, we'll handle this later if user have  repors
            ctask = 0
            itask = 0
        else:
            # we'have reports, also we'll handle this once argo have reports
            completedtasks = 0
            needrecommtaks = 0
            for report in list(reversed(reports)):
                if report.is_completed_and_recommended:
                    completedTaskReports.append(report)
                    completedtasks += 1
                else:
                    # that means that report need recommendation
                    needrecommtaks += 1
            ctask = completedtasks
            itask = needrecommtaks + noreporttask
        
        completed_today = []
        for report in completedTaskReports:
            if report.added_on.date() == dt.date.today():
                completed_today.append(report)

        return render(request, self.template_name, {"argonomist": argonomist, "completed": completed_today, "assignedtask": len(ainfos)-completedTask, "ctask": len(completed_today), "itask": itask, "reports": reports, "idadi": len(reports), "fname": self.request.user.argonomic.first_name, "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})


completed_today = CompletedTaskToday.as_view()

class IncompleteTask(View):
    # HII LINK NI SAWA NA KUM-REDIRECT MTU KWENYE 'MY_TASK, BUT INABIDI TUWEKE UTOFAUTI HAPA INABIDI TU-RETURN ONLY DATA WHICH HAVE REPORTS...' 

    template_name = "argonomist/incompletetask.html"

    @method_decorator(permission_required('mkulima.view_argonprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        argonomist = self.request.user.argonomic
        reports = argonomist.argoreport.all()
        infos = GatheredInfo.objects.filter(isAssigned=False)
        reports = argonomist.argoreport.all()
        ainfos = GatheredInfo.objects.filter(assignedTo=argonomist)
        completedTaskReports = []  # these are just a reports
        completedTask = 0
        incompletedTasks = []
        for info in ainfos:
            farm = info.gatheredinfo
            report = farm.report.all()
            if len(report) > 0:
                print('now im here')
                print(report[len(report) - 1].is_completed_and_recommended)
                if report[len(report) - 1].is_completed_and_recommended == True:
                    # completedTaskReports.append(report[len(report) - 1])
                    completedTask += 1

        noreporttask = 0
        # i don't know why i'm having 2 for loops here
        for info in ainfos:
            farm = info.gatheredinfo
            report = farm.report.all()
            if (len(report) < 1):
                noreporttask += 1
                # kumbuka hizi hazina report but sisi hapa tunataka tu-display zenye report, info
                # {% comment %} HII LINK NI SAWA NA KUM-REDIRECT MTU KWENYE 'MY_TASK, BUT INABIDI TUWEKE UTOFAUTI HAPA INABIDI TU-RETURN ONLY DATA WHICH HAVE REPORTS...' {% endcomment %}
                # Tutaifanya baadae hii logic...
                incompletedTasks.append(info)
        if len(reports) < 1:
            # idadi ya task/report ni zero, we'll handle this later if user have  repors
            ctask = 0
            itask = 0
        else:
            # we'have reports, also we'll handle this once argo have reports
            completedtasks = 0
            needrecommtaks = 0
            for report in list(reversed(reports)):
                if report.is_completed_and_recommended:
                    completedTaskReports.append(report)
                    completedtasks += 1
                else:
                    # that means that report need recommendation
                    needrecommtaks += 1
                    incompletedTasks.append(report.farm.farm_metadata)
            ctask = completedtasks
            # but hii inakuwa haina tofauti na my_task... otherwiser kama vipi tuitoe hii coz its the same to my task..
            itask = needrecommtaks + noreporttask

        # print(completedTaskReports, ' completedReports..')
        print('incomplete tasks assigned i picked ', incompletedTasks)
        return render(request, self.template_name, {"incompletetasks": incompletedTasks, "argonomist": argonomist, "completed": completedTaskReports, "assignedtask": len(ainfos)-completedTask, "ctask": ctask, "itask": itask,  "atask": len(infos), "reports": reports, "idadi": len(reports), "fname": self.request.user.argonomic.first_name, "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})

incomplete_task = IncompleteTask.as_view()


class ArgonomistProfile(View):
    template_name = 'argonomist/full_profile.html'

    # mi ninavyojua dispatch ni kama 'initialize'/constructor function, ko we add protection in our view here
    @method_decorator(permission_required('mkulima.view_argonprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        argonomist = self.request.user.argonomic
        reports = argonomist.argoreport.all()
        infos = GatheredInfo.objects.filter(isAssigned=False)
        reports = argonomist.argoreport.all()
        ainfos = GatheredInfo.objects.filter(assignedTo=argonomist)
        completedTaskReports = []  # these are just a reports
        completedTask = 0

        for info in ainfos:
            farm = info.gatheredinfo
            report = farm.report.all()
            if len(report) > 0:
                print('now im here')
                print(report[len(report) - 1].is_completed_and_recommended)
                if report[len(report) - 1].is_completed_and_recommended == True:
                    # completedTaskReports.append(report[len(report) - 1])
                    completedTask += 1

        noreporttask = 0
        # i don't know why i'm having 2 for loops here
        for info in ainfos:
            farm = info.gatheredinfo
            report = farm.report.all()
            if (len(report) < 1):
                noreporttask += 1
        if len(reports) < 1:
            # idadi ya task/report ni zero, we'll handle this later if user have  repors
            ctask = 0
            itask = 0
        else:
            # we'have reports, also we'll handle this once argo have reports
            completedtasks = 0
            needrecommtaks = 0
            for report in list(reversed(reports)):
                if report.is_completed_and_recommended:
                    completedTaskReports.append(report)
                    completedtasks += 1
                else:
                    # that means that report need recommendation
                    needrecommtaks += 1
            ctask = completedtasks
            itask = needrecommtaks + noreporttask

        completed_today = []
        for report in completedTaskReports:
            if report.added_on.date() == dt.date.today():
                completed_today.append(report)


        print(completedTaskReports, ' completedReports..')
        return render(request, self.template_name, {"ctoday": len(completed_today), "argonomist": argonomist, "completed": completedTaskReports, "assignedtask": len(ainfos)-completedTask, "ctask": ctask, "itask": itask,  "atask": len(infos), "reports": reports, "idadi": len(reports), "fname": self.request.user.argonomic.first_name, "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})


class TestRecord(View):
    template_name = 'argonomist/testrecord.html'

    @method_decorator(permission_required('mkulima.view_argonprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        info_id = self.kwargs.get('rid')
        info = GatheredInfo.objects.get(id=int(info_id))
        gatheredinfos = GatheredInfo.objects.all()
        owner = info.owner
        coors = info.coordinates
        # print('dirs ', dir(info))
        # print('farm size ', info.programmed_farmsize)
        argonomist = self.request.user.argonomic
        return render(request, self.template_name, {"info": info, "argonomist": argonomist.id, "owner": owner, "farm": info.gatheredinfo, "coords": json.loads(coors.allCoords), "infolen": gatheredinfos.count(), "id": info_id, "fname": self.request.user.argonomic.first_name, "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})


test_record = TestRecord.as_view()


class MyTask(View):
    template_name = 'argonomist/my_task.html'

    @method_decorator(permission_required('mkulima.view_argonprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # information assigned to this argo
        user = self.request.user
        argonomist = user.argonomic
        '''
            unajua .all() inakua available in foreignRelation and manyTomanyrelation but not in the
            onetoone relation since onetoone relation is locked to only one record/data.. to access
            the record in onetoone relation is 'argonomist.assignedto' but in foreignKey and manytomany
            relation we need to use .all() so as to get all records...

            also you should understand that in first case if you try to get record argonomist.assignedto which not added yet it
            return error.. is just using .get() method to access unknown id of record instead of doing like
            in nodejs where it return 'undefined' it return 'error'...

            in second case of foreign and manytomany if you try to access record which is not added using .all()
            it will return []
        '''
        my_task = argonomist.assignedto.all()
        incompletedTask = []
        for task in my_task:
            farm = task.gatheredinfo
            report = farm.report.all()
            if len(report) > 0:
                repo = report[len(report) - 1]
                if repo.is_completed_and_recommended:
                    continue
                else:
                    incompletedTask.append(task)
            else:
                incompletedTask.append(task)
        # print(incompletedTask, len(incompletedTask))
        infos = GatheredInfo.objects.filter(isAssigned=False)
        return render(request, self.template_name, {"argonomist": argonomist.id, "atask": len(infos), "idadincompletetask": len(incompletedTask), "tasks": reversed(incompletedTask), "fname": self.request.user.argonomic.first_name, "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})


my_task = MyTask.as_view()


class ArgonomicsAddTest(View):
    template_name = 'argonomist/addtest.html'

    # mi ninavyojua dispatch ni kama 'initialize'/constructor function, ko we add protection in our view here
    @method_decorator(permission_required('mkulima.view_argonprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        gatheredinfos = GatheredInfo.objects.filter(
            isAssigned=False)
        print('gathered infors ', gatheredinfos)
        return render(request, self.template_name, {"argonomist": self.request.user.argonomic, "infolen": gatheredinfos.count(), "gatheredinfos": reversed(gatheredinfos), "fname": self.request.user.argonomic.first_name, "lname": self.request.user.argonomic.last_name, "photo": self.request.user.argonomic.profile_picture.url})


class CreateArgonomistProfile(View):
    # https://stackoverflow.com/questions/36610146/attributeerror-file-object-has-no-attribute-committed
    # hii error inasababishwa an FileField in your models for 'attachment' field sijui maanke ni nini
    # Pass in the filename and content to the FileField's save() method directly, rather than using the model instance's save() method.
    template_name = 'argonomist/add_profile.html'

    def get(self, request):
        try:
            if (self.request.user.email):  # if user has no loged in it return 'AnonymousUser' obj which does not hafe 'email' attribute so it will raise error if you try to access it, unlike js which return 'undefined' django it 'throw' an error if 'key' is not found... so we should handle this will try---except statement and if it catch then we know its 'AnonymousUser' obj then we'll redirect user to login form....
                return render(request, self.template_name)
        except Exception as err:
            # that's is anonymous user
            return HttpResponseRedirect(reverse('login'))

        return HttpResponseRedirect(reverse('login'))

    def post(self, request):
        fname = request.POST.get('fname', None)
        lname = request.POST.get('lname', None)
        phone = request.POST.get('phone', None)
        country = request.POST.get('country', None)
        region = request.POST.get('region', None)
        district = request.POST.get('district', None)
        ward = request.POST.get('ward', None),
        pic = request.FILES.get('profile', None)
        education = request.POST.get('e-level', None)
        cert = request.FILES.get('certificate', None)

        # get all admins which are recievers to verify new argonomist...
        users_qs = get_user_model().objects.all()
        admins = []
        for account in users_qs:
            if hasattr(account, "adminprofile"):
                admins.append(account)


        if fname and lname and phone and country and region and district and ward and pic and education and cert:
            print(fname, lname,
                  phone, country,
                  region, district,
                  ward, pic,
                  education,
                  cert)

            try:
                int(phone)
            except Exception as err:
                # user hajapass number sahihi namba ya simu inabidi iwe string of 'integer' not decimal or anything like this.. kama akipass na country code like +2333839483932 itakataa coz '+' can't be parsed in integer
                print('errors in phone number')
                return render(request, self.template_name, {"message": "Make sure you pass phone number without country code"})

            if len(phone.strip()) != 10:
                print('errors in phone number')
                return render(request, self.template_name, {"message": "Phone number length should be 10"})

            try:
                try:
                    profile = ArgonProfile.objects.get(user=self.request.user)
                except Exception:
                    # Hapa hii scenario ni muhimu endapo profile la user limefutwa but user exist that means it tried to .get profile but it does not exist for that case we should create a new profile for  that user
                    profile = ArgonProfile.objects.create(
                        user=self.request.user,
                        user_group='Argonomist'
                    )
                profile.profile_picture = File(pic)
                profile.first_name = fname
                profile.last_name = lname
                profile.phone = phone
                profile.country = country
                profile.education_level = education
                profile.region = region
                profile.district = district
                profile.ward = ''.join(ward)
                profile.attachment = File(cert)
                profile.profileIsCompleted = True
                print('I dont know what happen')
                profile.save()
                group = Group.objects.get(name='Argonomist')
                user = request.user
                user.groups.add(group)
                # every argonomist should pass here if he's not yet complete the profile
                # so its here where we need to make them 'inactive'
                user.is_active = False
                user.save()

                for admin in admins:
                    # create notification...
                    notification = Notification.objects.create(
                        receiver = admin,
                        subject = "New Argonomist Created",
                        body = """
                                New Argonomist have been created,.
                                The account of user will remain inactive waiting for your verification
                               """,
                        created_user = user.id,
                    )

                    notification.save()
                    
                
                # we should redirect to the page your account is under the review, wait to be verified
                return HttpResponseRedirect(reverse('waitingverification'))

            except Exception as err:
                print('error ', err)
                return render(request, self.template_name, {"message": err})

        else:
            print('error at the end')
            return render(request, self.template_name, {"message": "We don't accept empty fields"})


add_test = ArgonomicsAddTest.as_view()
access_profile = ArgonomistProfile.as_view()
argo_profile = CreateArgonomistProfile.as_view()
