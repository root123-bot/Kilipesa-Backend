from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from MkulimaBackend.mkulima.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_http_methods
from rest_framework import generics
from .serializers import *
# Create your views here.
from django.conf import settings
from django.core.mail import send_mail
import smtplib
from django.contrib.auth.models import Group
from rest_framework import status
import datetime as dt

import pytz
tztimezone = pytz.timezone("Africa/Dar_es_Salaam")


class CheckIfUserExistButInactive(APIView):
    def post(self, request, *args, **kwargs):
        try:
            email = request.data['email']
            user = get_user_model().objects.get(email=email)
            if (user.is_active == False):
                return Response(
                    {"status": True},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"status": False},
                    status=status.HTTP_200_OK
                )
        except Exception as err:
            return Response(
                {"details": str(err)},
                status=status.HTTP_400_BAD_REQUEST
            )

is_user_active = CheckIfUserExistButInactive.as_view()


class UpdateRecordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            record_id = request.data.get('record_id')
            record = GatheredInfo.objects.get(id=int(record_id))
            owner = record.owner
            coordinates = record.coordinates
            family = owner.family
            kin = owner.nextkin
            farm = record.gatheredinfo

            print(record, coordinates, owner, family, kin, farm)

            oname = request.data.get('oname', None)
            oage = request.data.get('oage', None)
            ogender = request.data.get('ogender', None)
            # hatutatuma ophoto if the user has not changed it 
            ophoto = request.data.get('ophoto', None)
            ophone = request.data.get('ophone', None)
            onida = request.data.get('onida', None)
            oregion = request.data.get('oregion', None)
            odistrict = request.data.get('odistrict', None)
            oward = request.data.get('oward', None)
            nkname = request.data.get('nkname', None)
            nkage = request.data.get('nkage', None)
            # oname = request.data.get('oname', None)
            nkphone = request.data.get('nkphone', None)
            nkgender = request.data.get('nkgender', None)
            nknida = request.data.get('nknida', None)
            fdchild = request.data.get('fdchild', "")
            fdwives = request.data.get('fdwives', "")
            fdlive = request.data.get('fdlive', "")
            fdhouse = request.data.get('fdhouse', None)
            fdmarital = request.data.get('fdmarital', None)

            fmdistrict = request.data.get('fmdistrict', None)
            fmregion = request.data.get('fmregion', None)
            fmward = request.data.get('fmward', None)

            currentuse = request.data.get('currentuse', None)
            currentcrop = request.data.get('currentcrop', None)
            averageyield = request.data.get('averageyield', None)
            lh = request.data.get('coords', None)

            if onida == 'null':
                onida = None
            
            if nknida == "null":
                nknida = None


            print({
                "oname": oname,
                "ogender": ogender,
                "oage": oage,
                "ophoto": ophoto,
                "ophone": ophone,
                "onida": onida,
                "oregion": oregion,
                "odistrict": odistrict,
                "oward": oward,
                "nkname": nkname,
                "nkage": nkage,
                "nkphone": nkphone,
                "nkgender": nkgender,
                "fdmarital": fdmarital,
                "fdhouse": fdhouse,
                "fmdistrict": fmdistrict,
                "fmregion": fmregion,
                "fmward": fmward,
                "currentuse": currentuse,
                "lh": lh
            })

            if (oname and ogender and oage and ophone  
                and oregion and odistrict and oward and nkname and nkage
                and nkphone and nkgender and fdmarital and fdhouse and 
                fmdistrict and fmregion and fmward and currentuse and lh):
                
                try: 
                    family.martial_status = fdmarital
                    family.noChild = int(fdchild) if len(fdchild.strip()) > 0 else 0
                    family.noWives=int(fdwives) if len(fdwives.strip()) > 0 else 0
                    family.nolivestock = int(fdlive) if len(fdlive.strip()) > 0 else 0
                    family.houseType=fdhouse
                
                    family.save()

                    # if you put ',' it will save the data as a tuple, for example i put owner.phone = phone, then it 
                    # save data as ('phone') instead of phone
                    try:
                        owner.full_name = oname
                        owner.age=int(oage)
                        owner.gender=ogender
                        owner.phone=ophone
                        owner.nationalID=None if onida == None else onida
                        owner.country='TANZANIA'
                        owner.region=oregion
                        owner.district=odistrict
                        owner.ward=oward
                        if (ophoto != 'null' and ophoto != None ):
                            print('there is photo posted ', ophoto, type(ophoto), ophoto != None, ophoto == None)
                            owner.photo=ophoto

                        owner.save()

                        try:
                            kin.full_name=nkname
                            kin.age=int(nkage)
                            kin.phone=nkphone
                            kin.gender=nkgender
                            kin.nationalID=None if nknida == None else nknida
                    
                            kin.save()

                            try:
                                coordinates.allCoords = lh
                                coordinates.save()

                                try:
                                    record.owner = owner
                                    record.coordinates = coordinates
                                    record.save()

                                    try:
                                        farm.current_use = currentuse
                                        farm.current_crop = currentcrop
                                        farm.average_yield = averageyield
                                        farm.country = 'TANZANIA'
                                        farm.region = fmregion
                                        farm.district = fmdistrict
                                        farm.ward = fmward
                                
                                        farm.save()
                                    
                                        serializer = GatheredInfoSerializer(record)
                                        # photo found in our serializer..
                                        return Response(serializer.data, status=status.HTTP_200_OK)

                                    except Exception as err:
                                        # this means other metadata saved except this...
                                        print('farm error ', err)
                                        return Response({"details": str(err)}, status=status.HTTP_400_BAD_REQUEST)
                                
                                except Exception as err:
                                    print('record error ', err)
                                    return Response({"details": str(err)}, status=status.HTTP_400_BAD_REQUEST)

                            except Exception as err:
                                print('coord error ', err)
                                return Response({"details": str(err)}, status=status.HTTP_400_BAD_REQUEST)

                        except Exception as err:
                            print('kin error ', err)
                            return Response({"details": str(err)}, status=status.HTTP_400_BAD_REQUEST)
                    
                    except Exception as err:
                        print('owner error ', err)
                        return Response({"details": str(err)}, status=status.HTTP_400_BAD_REQUEST)
                    

                except Exception as err:
                    print('family error ', err)
                    return Response({"details": str(err)}, status=status.HTTP_400_BAD_REQUEST)


            else:
                print('some fields missing ')
                print({
                "oname": oname,
                "ogender": ogender,
                "oage": oage,
                "ophoto": ophoto,
                "ophone": ophone,
                "onida": onida,
                "oregion": oregion,
                "odistrict": odistrict,
                "oward": oward,
                "nkname": nkname,
                "nkage": nkage,
                "nkphone": nkphone,
                "nkgender": nkgender,
                "fdmarital": fdmarital,
                "fdhouse": fdhouse,
                "fmdistrict": fmdistrict,
                "fmregion": fmregion,
                "fmward": fmward,
                "currentuse": currentuse,
                "lh": lh
                })

                return Response({"details": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as err:
            print('error ', err)
            print({
                "oname": oname,
                "ogender": ogender,
                "oage": oage,
                "ophoto": ophoto,
                "ophone": ophone,
                "onida": onida,
                "oregion": oregion,
                "odistrict": odistrict,
                "oward": oward,
                "nkname": nkname,
                "nkage": nkage,
                "nkphone": nkphone,
                "nkgender": nkgender,
                "fdmarital": fdmarital,
                "fdhouse": fdhouse,
                "fmdistrict": fmdistrict,
                "fmregion": fmregion,
                "fmward": fmward,
                "currentuse": currentuse,
                "lh": lh
            })
            return Response({"error": err}, status=status.HTTP_400_BAD_REQUEST)


update_record = UpdateRecordAPIView.as_view()

class AddRecordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('id', None)
            user = get_user_model().objects.get(id=int(user_id))
            gatherman = GatherProfile.objects.get(user=user)

            oname = request.data.get('oname', None)
            oage = request.data.get('oage', None)
            ogender = request.data.get('ogender', None)
            ophoto = request.data.get('ophoto', None)
            ophone = request.data.get('ophone', None)
            onida = request.data.get('onida', None)
            oregion = request.data.get('oregion', None)
            odistrict = request.data.get('odistrict', None)
            oward = request.data.get('oward', None)
            nkname = request.data.get('nkname', None)
            nkage = request.data.get('nkage', None)
            # oname = request.data.get('oname', None)
            nkphone = request.data.get('nkphone', None)
            nkgender = request.data.get('nkgender', None)
            nknida = request.data.get('nknida', None)
            fdchild = request.data.get('fdchild', "")
            fdwives = request.data.get('fdwives', "")
            fdlive = request.data.get('fdlive', "")
            fdhouse = request.data.get('fdhouse', None)
            fdmarital = request.data.get('fdmarital', None)

            fmdistrict = request.data.get('fmdistrict', None)
            fmregion = request.data.get('fmregion', None)
            fmward = request.data.get('fmward', None)

            currentuse = request.data.get('currentuse', None)
            currentcrop = request.data.get('currentcrop', None)
            averageyield = request.data.get('averageyield', None)
            lh = request.data.get('coords', None)

            if (oname and ogender and oage and ophoto and ophone  
                and oregion and odistrict and oward and nkname and nkage
                and nkphone and nkgender and fdmarital and fdhouse and 
                fmdistrict and fmregion and fmward and currentuse and lh):


                print({
                    "oname" : oname, "ogender": ogender, "oage" : oage, "ophoto": ophoto,
                    "ophone": ophone,
                    "oregion": oregion, "odistrict": odistrict, "oward": oward,
                     "nkname" : nkname,
                      "nkage": nkage,
                    "nkphone": nkphone, "nkgender": nkgender, "marital": fdmarital,
                    "fdhouse":fdhouse,
                    "fmdistrict": fmdistrict, "fmregion": fmregion, "fmward": fmward,
                    "currentuse": currentuse, "coords": lh
                })
                try:
                    family = FamilyDetails.objects.create(
                        martial_status=fdmarital,
                        noChild=int(fdchild) if len(fdchild.strip()) > 0 else 0,
                        noWives=int(fdwives) if len(fdwives.strip()) > 0 else 0,
                        nolivestock = int(fdlive) if len(fdlive.strip()) > 0 else 0,
                        houseType=fdhouse,
                    )

                    family.save()  

                    try:
                        nextkin = NextKeen.objects.create(
                            full_name=nkname,
                            age=int(nkage),
                            phone=nkphone,
                            gender=nkgender,
                            national_ID=nknida if len(nknida.strip()) > 1 else None,
                        )
                        nextkin.save()
                        
                        try:
                            owner = Owner.objects.create(
                                full_name=oname,
                                age=int(oage),
                                gender=ogender,
                                phone=ophone,
                                nationalID=onida if len(onida.strip()) > 1 else None,
                                family=family,
                                nextkin=nextkin,
                                country='TANZANIA',
                                region=oregion,
                                district=odistrict,
                                ward=oward,
                                photo = ophoto,
                            )
                            owner.save()
                            
                            try:
                                size = Size.objects.create(
                                    allCoords = lh
                                )
                                size.save()

                                try:
                                    gatheredinfo = GatheredInfo.objects.create(
                                        owner=owner,
                                        gathered_by=gatherman,
                                        coordinates = size,
                                        added_on=dt.datetime.now(tztimezone),
                                    )
                                    gatheredinfo.save()

                                    
                                        
                                    try:
                                        farm = Farm.objects.create(
                                            farm_metadata = gatheredinfo,
                                            current_use=currentuse,
                                            current_crop=None if len(currentcrop.strip()) < 0 else currentcrop,
                                            average_yield=averageyield,
                                            country = 'TANZANIA',
                                            region = fmregion,
                                            district = fmdistrict,
                                            ward = fmward,
                                        )
                                        farm.save()

                                        serializer = GatheredInfoSerializer(gatheredinfo)
                                        return Response(
                                            serializer.data,
                                            status=status.HTTP_200_OK
                                        )
                                    except Exception as err:
                                        print('error farm ', err)
                                        return Response({"details": str(err)}, status=status.HTTP_400_BAD_REQUEST)

                                except Exception as err:
                                    print('error gatheredinfo ', err)
                                    return Response({"details": str(err)}, status=status.HTTP_400_BAD_REQUEST)


                            except Exception as err:
                                print('error size ', err)
                                return Response({"details": str(err)}, status=status.HTTP_400_BAD_REQUEST)

                        except Exception as err:
                            print('error owner ', err)
                            return Response({"details": str(err)}, status=status.HTTP_400_BAD_REQUEST)


                    except Exception as err:
                        print('error nextkin ', err)
                        return Response({"details": str(err)}, status=status.HTTP_400_BAD_REQUEST)

                except Exception as err:
                    print('error family ', err) 
                    return Response({"details": str(err)}, status=status.HTTP_400_BAD_REQUEST)

                
            else:
                print({
                    "oname" : oname, "ogender": ogender, "oage" : oage, "ophoto": ophoto,
                    "ophone": ophone,
                    "oregion": oregion, "odistrict": odistrict, "oward": oward,
                     "nkname" : nkname,
                      "nkage": nkage,
                "nkphone": nkphone, "nkgender": nkgender, "marital": fdmarital,
                 "fdhouse":fdhouse,
                 "fmdistrict": fmdistrict, "fmregion": fmregion, "fmward": fmward,
                  "currentuse": currentuse, "coords": lh
                })
                return Response(
                    {"details": "Missing some mandatory fields"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as err:
            return Response(
                {"details": str(err)},
                status=status.HTTP_400_BAD_REQUEST
            )

add_record_api = AddRecordAPIView.as_view()




class ChangePasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data['id']
            user = get_user_model().objects.get(id=int(user_id))
            old_password = request.data['old_password']
            new_password = request.data['new_password']
            confirm_password = request.data['confirm_password']

            if new_password != confirm_password:
                return Response(
                    {"details": "New password and confirm password does not match"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not user.check_password(old_password):
                return Response(
                    {"details": "Old password is incorrect"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(new_password)
            user.save()

            return Response(
                {"success": "Password changed successfully"},
                status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {"details": str(err)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
change_gpassword = ChangePasswordAPIView.as_view()

class EditGathermanProfile(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data['id']
            user = get_user_model().objects.get(id=int(user_id))
            gatherman = GatherProfile.objects.get(user=user)

            fname = request.data['fname']
            lname = request.data['lname']
            phone = request.data['phone']
            region = request.data['region']
            district = request.data['district']
            ward = request.data['ward']
            profile = request.data['profile']
            profile = profile if profile != "Use Old" else None

            gatherman.first_name = fname
            gatherman.last_name = lname
            gatherman.phone = phone
            gatherman.region = region
            gatherman.district = district
            gatherman.ward = ward
            if profile:
                gatherman.profile_picture = profile
            gatherman.save()

            serializer = GathermanSerializer(gatherman)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {"details": str(err)},
                status=status.HTTP_400_BAD_REQUEST
            )

edit_gatherman_profile = EditGathermanProfile.as_view()


class GatheredInfosByGatherman(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data['id']
            user = get_user_model().objects.get(id=int(user_id))
            gatherman = GatherProfile.objects.get(user=user)

            myinfos = GatheredInfo.objects.filter(gathered_by = gatherman)

            serializer = GatheredInfoSerializer(myinfos, many=True)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {"details": str(err)},
                status=status.HTTP_400_BAD_REQUEST
            )

my_info = GatheredInfosByGatherman.as_view()

class GathermanBio(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data['id']
            user = get_user_model().objects.get(id=int(user_id))
            gatherman = GatherProfile.objects.get(user=user)

            serializer = GathermanSerializer(gatherman)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {"details": str(err)},
                status=status.HTTP_400_BAD_REQUEST
            )

gatherman_bio = GathermanBio.as_view()

class FarmerOwnerBio(APIView):
    def post(self, request, *args, **kwargs):
        # ok you receive owner_id...  what you gonna do...
        try:
            owner_id = request.data['id']
            owner = Owner.objects.get(id=int(owner_id))

            serializer = FarmOwnerSerializer(owner)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        
        except Exception as err:
            return Response(
                {"details": str(err)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
farmer_bio = FarmerOwnerBio.as_view()

class UserStatus(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data['id']
            user = get_user_model().objects.get(id=int(user_id))

            return Response(
                {"status": user.is_active},
                status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {"details": str(err)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
user_status = UserStatus.as_view()
    

class CompleteGatherProfileAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print('SOMEONE NEED TO CREATE A PROFILE.. ', request.data)
        user_id = request.data.get('id', None)
        fname = request.data.get('fname', None)
        lname = request.data.get('lname', None)
        phone = request.data.get('phone', None)
        region = request.data.get('region', None)
        district = request.data.get('district', None)
        ward = request.data.get('ward', None)
        education_lv = request.data.get('education', None)
        certificate = request.data.get('certificate', None)
        profile = request.data.get('profile', None)
        print({
                    "fname", fname,
                    "lname", lname,
                    "phone", phone,
                    "region", region,
                    "district", district,
                    "ward", ward,
                    "education_lv", education_lv,
                    "certificate", certificate, 
                    "profile", profile
                })
        try: 
            if fname and lname and phone and region and district and ward and education_lv and certificate and profile:
                print({
                    "fname", fname,
                    "lname", lname,
                    "phone", phone,
                    "region", region,
                    "district", district,
                    "ward", ward,
                    "education_lv", education_lv,
                    "certificate", certificate, 
                    "profile", profile
                })
                # check how did you saved the images/files in django from frontend
                if (profile == 'null' or certificate == 'null'):
                    print('somethign went wrong')
                    # return Response of type error you should provide media file..
                    return Response(
                        {"details": "One of file or both are missing"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                user = get_user_model().objects.get(id=int(user_id))
                gatherman = GatherProfile.objects.get(
                    user = user
                )

                gatherman.first_name = fname
                gatherman.last_name = lname
                gatherman.phone = phone
                gatherman.region = region
                gatherman.district = district
                gatherman.ward = ward
                gatherman.education_level = education_lv
                gatherman.profile_picture = profile
                gatherman.attachment = certificate
                gatherman.profileIsCompleted = True
                gatherman.save()
                group = Group.objects.get(name='Gatherman')
                user.groups.add(group)
                user.is_active = False
                user.save()

                users_qs = get_user_model().objects.all()
                admins = []
                for account in users_qs:
                    if hasattr(account, "adminprofile"):
                        admins.append(account)

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
                
                return Response(
                    {"details": "Profile saved successfully"},
                    status=status.HTTP_200_OK
                )
            else:
                print('i dont know')
                return Response(
                    {"details": "All fields are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as err:
            print('error ', err)
            return Response(
                {"details": str(err)},
                status=status.HTTP_400_BAD_REQUEST
            )

create_gather_api = CompleteGatherProfileAPIView.as_view()

class FetchFarm(APIView):
    def post(self, request, *args, **kwargs):
        farm_id = request.data['id']
        farm = Farm.objects.get(id=int(farm_id))

        serializer = FarmSerializer(farm)
        return Response(serializer.data, status=status.HTTP_200_OK)


farm_detail = FetchFarm.as_view()


def mailing(recipient):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login('paschalnzwanga2015@gmail.com', 'syndpyznptrybjhn')

    smtpObj.sendmail('paschalnzwanga2015@gmail.com',
                     recipient, 'Subject: Hi my name is Slim Shady')
    smtpObj.quit()


def mail(request):
    mailing("stammeringprogrammmer@gmail.com")

    return HttpResponseRedirect('/')


class ListOfRecomms(generics.ListAPIView):
    queryset = Recommendations.objects.all()
    serializer_class = RecommendationSerializer


recomms = ListOfRecomms.as_view()


class ListOfFarms(generics.ListAPIView):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer

#


class ListOfRegions(generics.ListAPIView):
    queryset = regions.objects.all()
    serializer_class = RegionSerializers


class ListOfDistrict(generics.ListAPIView):
    queryset = districts.objects.all()
    serializer_class = DistrictSerializers


'''
    Avoid having the name of you're views to be the same to those of 'models' since it will bring the 
    AttributeError: 'districts' object has no attribute 'get'
    [17/Apr/2023 18:58:46] "GET /api/districts/ HTTP/1.1" 500 68299
    https://stackoverflow.com/questions/72022940/attributeerror-in-django-object-has-no-attribute-get
    for example i have that error when my model is 'districts' and my view is 'districts' since it will bring 
    confusion on importin' maybe instead of importing the models it might import the views and vice versa when it 
    try to import view it import the 'model' this is due to havign the model and views in the same name...
    
'''
mikoa = ListOfRegions.as_view()
wilaya = ListOfDistrict.as_view()


@require_http_methods(['HEAD', 'GET'])
def logoutuser(request):
    logout(request)
    return redirect('/')


class IndexView(View):
    template_name = "mkulima/index.html"

    def get(self, request):
        print(self.request.user, ' is there is a user')
        user = self.request.user
        try:

            email = self.request.user.email
            print('this is email of the user ', email)
            if (hasattr(user, 'gather')):
                return render(request, self.template_name, {"status": True, 'usetype': 'gather'})
            if (hasattr(user, 'argonomic')):
                return render(request, self.template_name, {"status": True, 'usetype': 'argo'})
            if (user.is_superuser):
                return render(request, self.template_name, {"status": True, 'usetype': 'admin'})

        except Exception as err:
            print('there is an error')
            return render(request, self.template_name, {"status": False})


index_view = IndexView.as_view()


class AboutView(View):
    template_name = "mkulima/about.html"

    def get(self, request):
        print(self.request.user, ' is there is a user')
        user = self.request.user
        try:
            email = self.request.user.email
            if (hasattr(user, 'gather')):
                return render(request, self.template_name, {"status": True, 'usetype': 'gather'})
            if (hasattr(user, 'argonomic')):
                return render(request, self.template_name, {"status": True, 'usetype': 'argo'})
            if (user.is_superuser):
                return render(request, self.template_name, {"status": True, 'usetype': 'admin'})

        except Exception as err:
            print('there is an error')

            return render(request, self.template_name, {"status": False})


about_view = AboutView.as_view()


class IndexView(View):
    template_name = 'mkulima/index.html'

    def get(self, request):
        return render(request, self.template_name)


class CreateAccountView(View):
    template_name = 'mkulima/register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        cat = request.POST.get('category', None)

        if email and password and cat:
            try:
                password_hash = make_password(password)

                user = get_user_model().objects.create(
                    email=email,
                    password=password_hash
                )

                user.save()
                if (cat == 'Argonomist'):
                    argonomist = ArgonProfile.objects.create(
                        user=user,
                        user_group='Argonomist'
                    )
                    argonomist.save()
                    login(request, user)
                    print('Im creating argonomist account..')
                    return HttpResponseRedirect(reverse('argo_profile'))
                elif (cat == 'Gatherman'):
                    gatherman = GatherProfile.objects.create(
                        user=user,
                        user_group='Gatherman'
                    )
                    gatherman.save()
                    login(request, user)
                    return HttpResponseRedirect(reverse('gather_profile'))

                else:
                    return render(request, self.template_name, {"message": "Error, pick user category"})
            except Exception as err:
                print('exception ', err)
                return render(request, self.template_name, {"message": "User with that email already exist"})

        return render(request, self.template_name, {"message": "We don't accept empty fields"})


class LoginView(View):
    template_name = 'mkulima/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        print(email, password)
        if email and password:
            # at first we shoul check if the user tries to login is 'active' or not.. lets check if there
            # is user with that email
            check = get_user_model().objects.filter(email=email)
            print('user existed ', check, check.count())
            if (check.count() > 0 and check[0].is_active == False):
                print('still inside')
                return HttpResponseRedirect(reverse('waitingverification'))

            # aunthenticate it return None by default if user is not_activated so we have our logic above to check if email exist then user exist..
            user = authenticate(request, username=email, password=password)

            if user is not None:

                if (hasattr(user, 'gather')):
                    login(request, user)
                    if (user.gather.profileIsCompleted):
                        return HttpResponseRedirect(reverse('gather_full_profile'))
                    # next time its named 'gather full_profile)
                    return HttpResponseRedirect(reverse('gather_profile'))

                if (hasattr(user, 'argonomic')):
                    login(request, user)
                    if (user.argonomic.profileIsCompleted):
                        return HttpResponseRedirect(reverse('argo_full_profile'))

                    # next time its named 'argo full_profile'
                    return HttpResponseRedirect(reverse('argo_profile'))

                # if he's admin then redirect to admin panel
                if (hasattr(user, 'adminprofile')):
                    # lets redirect to system administrator page..
                    login(request, user)
                    return HttpResponseRedirect(reverse('administrator'))
                if (user.is_superuser):
                    login(request, user)
                    return HttpResponseRedirect('/admin')

                return render(request, self.template_name, {"message": "User group is not recognized!"})

            else:
                return render(request, self.template_name, {"message": 'Unable to login incorrect credentials'})
        else:
            return render(request, self.template_name, {"message": "We don't accept empty fields"})


farms = ListOfFarms.as_view()
create_user = CreateAccountView.as_view()
index_view = IndexView.as_view()
login_view = LoginView.as_view()


# API VIEWS...
class UserProfile(APIView):
    def post(self, request):
        try:
            id = request.data.get("id", None)
            if id:
                # fetch user profile
                user = get_user_model().objects.get(id=int(id))
                user_profile = user.mkulima
                serializer = ProfileSerializers(user_profile)
                return Response(serializer.data)

        except Exception as err:
            return Response({"error": err})


class CreateRecord(APIView):
    def post(self, request):
        try:
            location = request.data.get('location', None)
            size = request.data.get('size', None)
            soil = request.data.get('soil', None)
            user_id = request.data.get('id', None)

            if location and size and soil and user_id:
                farm = Shamba.objects.create(
                    location=location,
                    size=size,
                    soil=soil,
                )
                farm.save()
                user = get_user_model().objects.get(id=int(user_id))
                profile = user.mkulima
                profile.shamba.add(
                    farm
                )
                profile.save()
                return Response({"message": 'Shamba have been saved succesful', "shamba": farm})
            else:
                return Response({"error": 'Missing parameters'})
        except Exception as err:
            return Response({"error": err})


user_profile = UserProfile.as_view()
create_shamba = CreateRecord.as_view()
