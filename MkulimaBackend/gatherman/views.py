from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from MkulimaBackend.mkulima.models import *
from MkulimaBackend.mkulima.models import GatherProfile as Profile
from django.core.files import File
import datetime as dt
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import json
import sys
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import login


from django.contrib.auth.models import Group

import pytz
tztimezone = pytz.timezone("Africa/Dar_es_Salaam")


class ChangePassword(View):
    template_name = "gatherman/changepassword.html"

    @method_decorator(permission_required('mkulima.view_gatherprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        gatherman = self.request.user.gather
        return render(request, self.template_name, {"gather": gatherman, "fname": self.request.user.gather.first_name, "lname": self.request.user.gather.last_name, "photo": self.request.user.gather.profile_picture.url})

    def post(self, request):
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user = self.request.user
        gatherman = user.gather

        print(request.POST.get('password'), request.POST.get(
            'password1'), request.POST.get('password2'))
        # sys.exit(1)
        # pass

        if (password1 != password2):
            return render(request, self.template_name, {"message": "Password didn\'t match", "gather": gatherman, "fname": self.request.user.gather.first_name, "lname": self.request.user.gather.last_name, "photo": self.request.user.gather.profile_picture.url})

        if (len(password1.strip()) < 6):
            return render(request, self.template_name, {"message": "Use longer password more than 6 characters is required", "gather": gatherman, "fname": self.request.user.gather.first_name, "lname": self.request.user.gather.last_name, "photo": self.request.user.gather.profile_picture.url})

        if user.check_password(password):
            user.password = make_password(password1)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("gather_full_profile"))

        # this means the old password is invalid..
        return render(request, self.template_name, {"message": "Error in changing password", "gather": gatherman, "fname": self.request.user.gather.first_name, "lname": self.request.user.gather.last_name, "photo": self.request.user.gather.profile_picture.url})


change_password = ChangePassword.as_view()


class EditProfile(View):
    template_name = 'gatherman/edit_profile.html'

    @method_decorator(permission_required('mkulima.view_gatherprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        gatherman = self.request.user.gather
        return render(request, self.template_name, {"gather": gatherman, "fname": self.request.user.gather.first_name, "lname": self.request.user.gather.last_name, "photo": self.request.user.gather.profile_picture.url})

    def post(self, request):
        gatherman = self.request.user.gather
        try:
            fname = request.POST.get('fname', None)
            lname = request.POST.get('lname', None)
            phone = request.POST.get('phone', None)
            country = request.POST.get('country', None)
            region = request.POST.get('region', None)
            district = request.POST.get('district', None)
            ward = request.POST.get('ward', None)
            profile = request.FILES.get('profilepicture', None)

            print({"fname": fname, "lname": lname, "phone": phone,
                   "country": country, "dist": district, "ward": ward,
                   "photo": profile})

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
            return HttpResponseRedirect(reverse('gather_full_profile'))
        except Exception as err:
            print('something went wrong ', err)
            return render(request, self.template_name, {"gather": gatherman, "fname": self.request.user.gather.first_name, "lname": self.request.user.gather.last_name, "photo": self.request.user.gather.profile_picture.url})


edit_profile = EditProfile.as_view()


class CreateNewRecord(View):
    template_name = 'gatherman/add_records.html'

    @method_decorator(permission_required('mkulima.view_gatherprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        gatherman = self.request.user.gather
        return render(request, self.template_name, {"gatherman": gatherman.id, "fname": self.request.user.gather.first_name, "lname": self.request.user.gather.last_name, "photo": self.request.user.gather.profile_picture.url})

    def post(self, request):
        lh = request.POST.get('lh', None)
        gatherman = self.request.user.gather

        oname = request.POST.get('oname', None)
        oage = request.POST.get('oage', None)
        ogender = request.POST.get('ogender', None)
        ophoto = request.FILES.get('ophoto', None)
        ophone = request.POST.get('ophone', None)
        onida = request.POST.get('onida', None)
        ocountry = request.POST.get('ocountry', None)
        oregion = request.POST.get('oregion', None)
        odistrict = request.POST.get('odistrict', None)
        oward = request.POST.get('oward', None)
        nkname = request.POST.get('nkname', None)
        nkage = request.POST.get('nkage', None)
        oname = request.POST.get('oname', None)
        nkphone = request.POST.get('nkphone', None)
        nkgender = request.POST.get('nkgender', None)
        nkphoto = request.FILES.get('nkphoto', None)
        nknida = request.POST.get('nknida', None)
        fdchild = request.POST.get('fdchild', 0)
        fdwives = request.POST.get('fdwives', 0)
        fdlive = request.POST.get('fdlive', 0)
        fdhouse = request.POST.get('fdhouse', None)
        fdmarital = request.POST.get('fdmarital', None)

        fmcountry = request.POST.get('fmcountry', None)
        fmdistrict = request.POST.get('fmdistrict', None)
        fmregion = request.POST.get('fmregion', None)
        fmward = request.POST.get('fmward', None)
        fmstreet = request.POST.get('fmstreet', None)
        # fmsize = request.POST.get('fmsize', None)

        currentuse = request.POST.get('currentuse', None)
        currentcrop = request.POST.get('currentcrop', None)
        averageyield = request.POST.get('averageyield', None)

        defaultDropdown = 'Open this select menu'
        print(currentcrop, currentuse, averageyield)
        if (oname and oage and (ogender != defaultDropdown) and ophone
            and ophoto and ocountry != defaultDropdown
            and (oregion != defaultDropdown) and (odistrict != defaultDropdown) and
            (oward != defaultDropdown) and nkname and nkage and (
                nkgender != defaultDropdown)
            and nkphone and
            (fmcountry != defaultDropdown) and (fmdistrict != defaultDropdown)
            and (fmregion != defaultDropdown) and (fmdistrict != defaultDropdown) and fmstreet and fdhouse and (
                fdmarital != defaultDropdown) and lh
                and currentuse):

            try:
                family = FamilyDetails.objects.create(
                    martial_status=fdmarital,
                    noChild=int(fdchild),
                    noWives=int(fdwives),
                    nolivestock=int(fdlive),
                    houseType=fdhouse
                )

                family.save()
                try:
                    nextkin = NextKeen.objects.create(
                        full_name=nkname,
                        gender=nkgender,
                        age=int(nkage),
                        phone=nkphone,
                        national_ID=nknida if len(nknida.strip()) > 1 else None,
                        photo=File(nkphoto)
                    )
                    nextkin.save()

                    try:
                        owner = Owner.objects.create(
                            full_name=oname,
                            age=int(oage),
                            gender=ogender,
                            nationalID=onida if len(onida.strip()) > 1 else None,
                            phone=ophone,
                            family=family,
                            nextkin=nextkin,
                            country=ocountry,
                            region=oregion,
                            district=odistrict,
                            ward=oward,
                            photo=File(ophoto)
                        )
                        owner.save()
                    except Exception as err:
                        print('Unable to save the Owner data ', err)
                        return render(request, self.template_name, {"message": err, "fname": self.request.user.gather.first_name, "lname": self.request.user.gather.last_name, "photo": self.request.user.gather.profile_picture.url})
                except Exception as err:
                    print('Exception ', err)
                    return render(request, self.template_name, {"gatherman": gatherman.id, "message": 'sth about age being 0 or negative is avoided'})

                size = Size.objects.create(
                    allCoords=lh
                )

                size.save()
                gatheredinfo = GatheredInfo.objects.create(
                    owner=owner,
                    gathered_by=self.request.user.gather,
                    coordinates=size,
                    added_on=dt.datetime.now(tztimezone),
                )
                gatheredinfo.save()

                try:
                    farm = Farm.objects.create(
                        farm_metadata=gatheredinfo,
                        current_use=currentuse,
                        current_crop=None if currentcrop == None else currentcrop,
                        average_yield=averageyield,
                        country=fmcountry,
                        region=fmregion,
                        district=fmdistrict,
                        ward=fmward,
                        street=fmstreet
                        # size=fmsize
                    )

                    farm.save()
                except Exception as err:
                    # unable to save the farm
                    print('ERROR IN SAVING FARM ... ', err)
                    return render(request, {"gatherman": gatherman.id, "message": err, "fname": self.request.user.gather.first_name, "lname": self.request.user.gather.last_name, "photo": self.request.user.gather.profile_picture.url})

                return HttpResponseRedirect(reverse('gather_full_profile'))

            except Exception as err:
                print('this is error to view ', err)
                return render(request, self.template_name, {"gatherman": gatherman.id, "message": err, "fname": self.request.user.gather.first_name, "lname": self.request.user.gather.last_name, "photo": self.request.user.gather.profile_picture.url})

        else:
            print('Some data is not valid')
            print({"oname": oname, "oage": oage, "ogender": ogender, "ophone": ophone, "ophoto": ophoto,
                   "onida": onida, "ocountry": ocountry, "oregion": oregion, "odistrict": odistrict,
                   "oward": oward, "nkname": nkname, "nkage": nkage, "nkgender": nkgender, "nkphone": nkphone,
                   "nkphoto": nkphoto, "nknida": nknida,
                   "fdhouse": fdhouse, "fdmartial": fdmarital,
                   "lh": lh, "currentuse": currentuse, "averageyield": averageyield})

        return render(request, self.template_name, {"gatherman": gatherman.id, "message": "You passed invalid data or empty data", "fname": self.request.user.gather.first_name, "lname": self.request.user.gather.last_name, "photo": self.request.user.gather.profile_picture.url})


class EditRecord(View):
    template_name = 'gatherman/edit_record.html'

    @method_decorator(permission_required('mkulima.view_gatherprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        record_id = self.kwargs.get('rid')
        gatheredInfos = GatheredInfo.objects.get(id=record_id)
        owner = gatheredInfos.owner
        kin = owner.nextkin
        family = owner.family
        coors = gatheredInfos.coordinates
        farm = gatheredInfos.gatheredinfo
        print('coors ', json.loads(coors.allCoords))

        user = self.request.user
        if hasattr(user, "adminprofile"):
            admin = user.adminprofile
            photo = admin.photo.url
            name = admin.name
            lname = ""
            user_group = "admin"
            gatherman_id = None
        else:
            gatherman = user.gather
            photo = gatherman.profile_picture.url
            name = gatherman.first_name
            lname = gatherman.last_name
            user_group = "Gatherman"
            gatherman_id = gatherman.id
        return render(request, self.template_name,
                      {"oname": owner.full_name, "crop": farm.current_crop,
                       "use": farm.current_use, "yield": farm.average_yield,
                       "coords": json.loads(coors.allCoords), "farm": farm,
                       "kin": kin, "owner": owner, "family": family,
                       "gatheredInfos": gatheredInfos, "fname": name,
                       "lname": lname, "photo": photo, "usergroup": user_group,
                       "gatherman": gatherman_id
                       })

    def post(self, request, *args, **kwargs):
        record_id = self.kwargs.get('rid')
        gatheredInfos = GatheredInfo.objects.get(id=record_id)
        owner = gatheredInfos.owner
        kin = owner.nextkin
        family = owner.family
        coors = gatheredInfos.coordinates
        farm = gatheredInfos.gatheredinfo

        try:
            # Our logic is to check if the django files exist if not then we should take or assume that the user used the default image... let's check...
            family.marital_status = request.POST.get('fdmarital', None)
            family.noChild = int(request.POST.get('fdchild', None))
            family.noWives = int(request.POST.get('fdwives', None))
            family.nolivestock = int(request.POST.get('fdlive', None))
            family.houseType = request.POST.get('fdhouse', None)
            family.save()

            kin.full_name = request.POST.get('nkname', None)
            kin.gender = request.POST.get('nkgender', None)
            kin.age = int(request.POST.get('nkage', None))
            kin.phone = request.POST.get('nkphone', None)
            kin.national_ID = request.POST.get('nknida', None)

            if (request.FILES.get('nkphoto', None)):
                kin.photo = File(request.FILES.get('nkphoto'))
            kin.save()

            owner.full_name = request.POST.get('oname', None)
            owner.age = int(request.POST.get('oage', None))
            owner.gender = request.POST.get('ogender', None)
            owner.nationalID = request.POST.get('onida', None)
            owner.country = request.POST.get('ocountry', None)
            owner.region = request.POST.get('oregion', None)
            owner.district = request.POST.get('odistrict', None)
            owner.ward = request.POST.get('oward', None)
            if (request.FILES.get('ophoto', None)):
                owner.photo = File(request.FILES.get('ophoto'))
            owner.save()

            coors.allCoords = request.POST.get('lh', None)

            coors.save()

            # let's hit the database for nothing like we save gathered info to see if added_on remain constant..
            gatheredInfos.updated_at = datetime.datetime.now(tztimezone)
            gatheredInfos.save()

            farm.current_use = request.POST.get('currentuse', None)
            farm.current_crop = request.POST.get('currentcrop', None)
            farm.average_yield = request.POST.get('averageyield', None)
            farm.country = request.POST.get('fmcountry', None)
            farm.district = request.POST.get('fmdistrict', None)
            farm.mward = request.POST.get('fmward', None)
            farm.region = request.POST.get('fmregion', None)
            farm.save()

            user = self.request.user
            if hasattr(user, "adminprofile"):
                return HttpResponseRedirect(reverse('farms'))

            else:
                return HttpResponseRedirect(reverse('gather_full_profile'))

        except Exception as err:
            print('Error occured ', err)
            return render(request, self.template_name, {"message": err, "oname": owner.full_name, "crop": farm.current_crop, "use": farm.current_use, "yield": farm.average_yield, "left": json.loads(coors.leftHeightContours), "right": json.loads(coors.rightHeightContours), "top": json.loads(coors.topWidthContours), "bottom": json.loads(coors.bottomWidthControus), farm: farm, "kin": kin, "owner": owner, "family": family, "gatheredInfos": gatheredInfos, "fname": self.request.user.gather.first_name, "lname": self.request.user.gather.last_name, "photo": self.request.user.gather.profile_picture.url})


class RecordsAddedToday(View):
    template_name = 'gatherman/output.html'

    @method_decorator(permission_required('mkulima.view_gatherprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        gather = self.request.user.gather
        gatheredInfos = GatheredInfo.objects.filter(
            gathered_by=gather)
        addedtoday = 0
        todayInfos = []
        for info in gatheredInfos:
            if info.added_on.date() == dt.date.today():
                addedtoday += 1
                todayInfos.append(info)
        return render(request, self.template_name, {"addedtoday": addedtoday, "gatherman": gather, "infolen": gatheredInfos.count(), "gatheredInfos": reversed(todayInfos), "fname": self.request.user.gather.first_name, "lname": self.request.user.gather.last_name, "photo": self.request.user.gather.profile_picture.url})

added_today = RecordsAddedToday.as_view()

class GatherProfile(View):
    template_name = 'gatherman/full_profile.html'

    @method_decorator(permission_required('mkulima.view_gatherprofile', raise_exception=True,))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        gather = self.request.user.gather
        gatheredInfos = GatheredInfo.objects.filter(
            gathered_by=gather)
        addedtoday = 0
        for info in gatheredInfos:
            if info.added_on.date() == dt.date.today():
                addedtoday += 1
        print('addedtoday ', addedtoday)
        return render(request, self.template_name, {"addedtoday": addedtoday, "gatherman": gather, "infolen": gatheredInfos.count(), "gatheredInfos": reversed(gatheredInfos), "fname": self.request.user.gather.first_name, "lname": self.request.user.gather.last_name, "photo": self.request.user.gather.profile_picture.url})


class CreateGatherProfile(View):

    template_name = 'gatherman/add_profile.html'

    def get(self, request):
        try:
            if (self.request.user.email):
                print(self.request.user.email)
                return render(request, self.template_name)
        except Exception as err:
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
                return render(request, self.template_name, {"message": "Make sure you pass phone number without country code"})

            if len(phone.strip()) != 10:
                return render(request, self.template_name, {"message": "Phone number length should be 10"})

            try:
                try:
                    profile = Profile.objects.get(user=self.request.user)
                except Exception:
                    # Hapa hii scenario ni muhimu endapo profile la user limefutwa but user exist that means it tried to .get profile but it does not exist for that case we should create a new profile for  that user
                    print('Its exception ', Profile)
                    profile = Profile.objects.create(
                        user=self.request.user,
                        user_group='Gatherman'
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

                profile.save()
                group = Group.objects.get(name='Gatherman')
                user = request.user
                user.groups.add(group)
                # all gatherman when they create the account will access this page to complete their profile...
                # what we need to do here is to 'deactivate' them for admin to activate them
                user.is_active = False
                user.save()
                for admin in admins:
                    # create notification...
                    notification = Notification.objects.create(
                        receiver = admin,
                        subject = "New Gatherman Created",
                        body = """
                                New gatherman have been created,.
                                The account of user will remain inactive waiting for your verification
                               """,
                        created_user = user.id,
                    )

                    notification.save()
                    
                return HttpResponseRedirect(reverse('waitingverification'))

            except Exception as err:
                print('error ', err)
                return render(request, self.template_name, {"message": err})

        else:
            return render(request, self.template_name, {"message": "We don't accept empty fields"})


edit_record = EditRecord.as_view()
create_record = CreateNewRecord.as_view()
access_profile = GatherProfile.as_view()
gather_profile = CreateGatherProfile.as_view()
