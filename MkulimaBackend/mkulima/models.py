from django.db import models
from django.contrib.auth import get_user_model
import datetime
from django.utils import timezone
import json
from area import area

SOIL_COLOR = [
    ('BLACK', 'BLACK'),
    ('RED', 'RED'),
    ('WHITE', 'WHITE'),
    ('BROWN', 'BROWN'),
    ('GREY', 'GREY'),
    ('YELLOW', 'YELLOW')
]


SOIL_FORM = [
    ('SAND', 'SAND'),
    ('SILT', 'SILT'),
    ('CLAY', 'CLAY'),
]

SOIL_STRUCTURE = [
    ('PLATY', 'PLATY'),
    ('PLISMATIC', 'PLISMATIC'),
    ('COLUMNAR', 'COLUMNAR'),
    ('GRANULAR', 'GRANULAR'),
    ('BLOCKY', 'BLOCKY'),
]

SOIL_TEXTURE = [
    ('SAND', 'SAND'),
    ('LOAMY SAND', 'LOAMY SAND'),
    ('SANDY LOAM', 'SANDY LOAM'),
    ('LOAM', 'LOAM'),
]

######### UPDATES ############
EDUCATION_LEVEL = [
    ('BACHELOR DEGREE', 'BACHELOR DEGREE'),
    ('DIPLOMA', 'DIPLOMA'),
    ('O-LEVEL', 'O-LEVEL'),
    ('A-LEVEL', 'A-LEVEL'),
]

USER_GROUP = [
    ('GATHER', 'GATHER'),
    ('ARGONOMIC', 'ARGONOMIC'),
    ('3RD PARTIES', '3RD PARTIES')
]

HOUSE_TYPE = [
    ('NYASI', 'NYASI'),
    ('BATI', 'BATI'),
    ('GOOD STANDARD', 'GOOD STANDARD'),
]



# what if the message viewed by another admin, do it will be shown viewed.. what do we need to do
# is to have a field "receiver" mandatory and we should create a notification instance for 
# each admin even if we've the same content.. so here the field of receiver is MANDATORY we can have
# sender 'blank' since some message are generated by the system.. THIS SCENARIO DETECTED since we want 
# to make or allow users/admins to delete and read notification..
class Notification(models.Model):
    sender = models.ForeignKey(get_user_model(), related_name="notification", on_delete=models.SET_NULL, blank=True, null=True)
    receiver = models.ForeignKey(get_user_model(), related_name="alert", on_delete=models.SET_NULL, blank=True, null=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    isViewed = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)
    created_user = models.CharField(max_length=50, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class GatherProfile(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, unique=True, related_name='gather')
    profile_picture = models.ImageField(
        verbose_name="Profile picture", upload_to='images/', default='images/profile.png', blank=True, null=True)
    first_name = models.CharField(max_length=500, blank=True, null=True)
    last_name = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=500, blank=True, null=True)
    region = models.CharField(max_length=500, blank=True, null=True)
    district = models.CharField(max_length=500, blank=True, null=True)
    ward = models.CharField(max_length=500, blank=True, null=True)
    street = models.CharField(
        help_text="Street/Village", max_length=500, blank=True, null=True)
    education_level = models.CharField(max_length=500, blank=True, null=True)
    # https://stackoverflow.com/questions/36610146/attributeerror-file-object-has-no-attribute-committed
    attachment = models.FileField(upload_to='files/', blank=True, null=True)
    user_group = models.CharField(
        max_length=500, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    profileIsCompleted = models.BooleanField(default=False)
    user_status = models.CharField(max_length=500, blank=True, null=True)

    # the user status can be "Active/Suspended/Inactive"
    @property
    def number_of_records(self):
        return self.gathered_by.all().count()
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def recordsaddedtoday(self):
        gatherdInfos = self.gathered_by.all()
        today = datetime.date.today()
        count = 0
        for gatherdInfo in gatherdInfos:
            if gatherdInfo.added_on.date() == today:
                count += 1
        
        return count

    @property
    def location(self):
        return f"{self.region}, {self.district}"
    
    @property
    def profile_pic(self):
        return self.profile_picture.url

    

class ArgonProfile(models.Model):
    user = models.OneToOneField(get_user_model(
    ), on_delete=models.CASCADE, unique=True, related_name='argonomic')
    profile_picture = models.ImageField(
        verbose_name="Profile picture", upload_to='images/', default='images/profile.png', blank=True, null=True)
    first_name = models.CharField(max_length=500, blank=True, null=True)
    last_name = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=500, blank=True, null=True)
    region = models.CharField(max_length=500, blank=True, null=True)
    district = models.CharField(max_length=500, blank=True, null=True)
    ward = models.CharField(max_length=500, blank=True, null=True)
    street = models.CharField(
        help_text="Street/Village", max_length=500, blank=True, null=True)
    education_level = models.CharField(max_length=500, blank=True, null=True)
    # https://stackoverflow.com/questions/36610146/attributeerror-file-object-has-no-attribute-committed
    attachment = models.FileField(upload_to='files/', blank=True, null=True)
    user_group = models.CharField(
        max_length=500, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    profileIsCompleted = models.BooleanField(default=False)
    user_status = models.CharField(max_length=500, blank=True, null=True)


    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def location(self):
        return f"{self.region}, {self.district}"

    @property
    def profile(self):
        return self.profile_picture.url

    @property
    def status(self):
        return self.user.is_active

    @property
    def tasks(self):
        tasks = self.argoreport.all()
        completed_tasks = []

        for task in tasks:
            if task.is_completed_and_recommended:
                completed_tasks.append(task)

        return len(completed_tasks)


class AdminProfile(models.Model):
    user = models.OneToOneField(get_user_model(
    ), on_delete=models.CASCADE, unique=True, related_name='adminprofile')
    name = models.CharField(max_length=50, blank=True,
                            null=True, default='#7323D923')
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    user_group = models.CharField(max_length=200, default="Admin")


# this should be an array of coords starting from left or right as origin to origin
class Size(models.Model):
    allCoords = models.CharField(max_length=1000000000)


class FamilyDetails(models.Model):
    martial_status = models.CharField(max_length=200, default="Married")
    noChild = models.IntegerField(blank=True, null=True)
    noWives = models.IntegerField(blank=True, null=True)
    nolivestock = models.IntegerField(blank=True, null=True)
    houseType = models.CharField(max_length=3000, choices=HOUSE_TYPE)
    added_at = models.DateTimeField(auto_now_add=True)


class FarmLocation(models.Model):
    country = models.CharField(max_length=800, null=True, blank=True)
    region = models.CharField(max_length=800, null=True, blank=True)
    district = models.CharField(max_length=800, null=True, blank=True)
    ward = models.CharField(max_length=800, null=True, blank=True)
    street = models.CharField(max_length=800, null=True, blank=True)
    size = models.CharField(
        max_length=800, help_text="Size in hectras", null=True, blank=True)

        
    
# one kins many family... one family many kins...


class NextKeen(models.Model):
    full_name = models.CharField(max_length=2000)
    age = models.IntegerField()
    gender = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    national_ID = models.CharField(max_length=500, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return "Next of kin " + self.full_name
# kama migration inasumbua provide default run migration to give value to already instance then remove default and run migration again itakubali na kila kitu kitaenda sawa..


class Owner(models.Model):
    full_name = models.CharField(max_length=8000)
    age = models.IntegerField()
    gender = models.CharField(max_length=8000)
    nationalID = models.CharField(max_length=8000, null=True, blank=True)
    phone = models.CharField(max_length=15)
    family = models.OneToOneField(
        FamilyDetails, on_delete=models.CASCADE, related_name="familydetails")
    nextkin = models.OneToOneField(
        NextKeen, on_delete=models.CASCADE, null=True, blank=True, related_name="nextkin")
    added_at = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=500)
    region = models.CharField(max_length=500)
    district = models.CharField(max_length=500)
    ward = models.CharField(max_length=500)
    street = models.CharField(
        help_text="Street/Village", max_length=500, blank=True, null=True)
    photo = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"Owner {self.full_name} => {self.id}"

    @property 
    def profile_pic(self):
        return self.photo.url

    @property
    def location(self):
        return f"{self.region}, {self.district}"

    @property
    def noOfFarms(self):
        name = self.full_name
        myfarms = []
        # find all farms which appear to have this nationalID in owner..
        farms = Farm.objects.all()
        for farm in farms:
            if farm.farm_metadata.owner.full_name == name:
                myfarms.append(farm)

        return len(myfarms)

    @property
    def totalSize(self):
        name = self.full_name
        totalsize = 0
        farms = Farm.objects.all()
        for farm in farms:
            if farm.farm_metadata.owner.full_name == name:
                totalsize += float(farm.pragrammed_farmsize)

        return totalsize


class GatheredInfo(models.Model):
    owner = models.ForeignKey(
        Owner, on_delete=models.CASCADE, related_name='farm_owner')
    # Haimake sense if we delete the gatherman to delete the gathered info
    # what we care most is info gathered than the who gather that info
    gathered_by = models.ForeignKey(
        GatherProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='gathered_by')
    # we get farm location and size by Coordinates...
    coordinates = models.OneToOneField(
        Size, on_delete=models.CASCADE, related_name="farm_coordinates", blank=True, null=True)
    # hii ina-change everytime we update/save instance
    gathered_at = models.DateTimeField(auto_now_add=True)
    added_on = models.DateTimeField()
    # hapa ndo inabidi tutumie auto_now_add=True since it update the 'date' everytime the instance is saved to the DB
    updated_at = models.DateTimeField(
        auto_now_add=True)
    # this is locking day and it should automatically be calculated from 'added_at' maybe plus 1 day...... locked for 'gatherman' to not edit it..
    # this field data also added when we add the updated_at in our views, for example I will say it should be
    # expired after 2 days so i will take time i want to put in updated_at and plus to it a couple of days.. this
    # handled programmatically when the user is in view
    assigned_at = models.DateTimeField(blank=True, null=True)
    assignedTo = models.ForeignKey(
        ArgonProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="assignedto")
    isAssigned = models.BooleanField(default=False)
    # this field data also added when we add the assigned_at in our views, for example I will say it should be
    # expired after 2 days so i will take time i want to put in assigned_at and plus to it a couple of days.. this
    # handled programmatically when the user is in view
    release_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.owner.full_name

    
    # hatuwezi ku-return data zote kupitia hii farm_owner id tuta-fetch other data pale user akitaka a-edit gathered_info..
    @property
    def farm_owner(self):
        return {
            "name": self.owner.full_name,
            "id": self.owner.id,
            "kinId": self.owner.nextkin.id,
            "familyId": self.owner.family.id
        }
    
    # hizi ids ni muhimu zinatusaidia ku-fetch other metadata.. vilevile tunavyo-edit records
    @property
    def get_coordinates(self):
        return {
            "coords": self.coordinates.allCoords,
            "coordsId": self.coordinates.id
        }            
    
    @property
    def farm(self):
        return {
            "farmId": self.gatheredinfo.id,
            "farm_location": f"{self.gatheredinfo.region}",
            "current_use": self.gatheredinfo.current_use,
            "current_crop": self.gatheredinfo.current_crop,
            "average_yield": self.gatheredinfo.average_yield,
        }

    @property
    def get_owner_info(self):
        owner = self.owner
        return {
            "id": owner.id,
            "full_name": owner.full_name,
            "age": owner.age,
            "gender": owner.gender,
            "nationalID": owner.nationalID if owner.nationalID else None,
            "phone": owner.phone,
            "region": owner.region,
            "district": owner.district,
            "ward": owner.ward,
            "photo": owner.photo.url
        }
    
    @property
    def farm_location(self):
        farm_info = self.gatheredinfo

        return {
            "id": farm_info.id,
            "region": farm_info.region,
            "district": farm_info.district,
            "ward": farm_info.ward,
        }
    
    @property
    def extra_info(self):
        farm_info = self.gatheredinfo

        return ({
            "cuse": farm_info.current_use,
            "ccrop": farm_info.current_crop if farm_info.current_crop else None,
            "yield": farm_info.average_yield if farm_info.average_yield else None
        })
    

    @property
    def nextkin_info(self):
        return {
            "id": self.owner.nextkin.id,
            "name": self.owner.nextkin.full_name,
            "age": self.owner.nextkin.age,
            "gender": self.owner.nextkin.gender,
            "phone": self.owner.nextkin.phone,
            "nationalID": self.owner.nextkin.national_ID if self.owner.nextkin.national_ID else None,
        }

    @property
    def family_details(self):
        family = self.owner.family
        return {
            "id": family.id,
            "marital_status": family.martial_status,
            "children": family.noChild,
            "noWives": family.noWives,
            "noLivestock": family.nolivestock,
            "houseType": family.houseType,
        }

    @property
    def programmed_farmsize(self):
        coordinates = self.coordinates.allCoords
        coords = []
        coordinates = json.loads(coordinates)
        for coordinate in coordinates:
            latlong = coordinate.split(',')
            latlong2 = []
            for element in latlong:
                latlong2.append(float(element))
            coords.append(latlong2)

        print(coords)
        # look like [[a,b], [c, d]]
        co = {
            'type': 'Polygon',
            'coordinates': [coords]
        }
        
        # area in meter square.
        return area(co)
    

'''
    this gathered information should be assigened to single "Argonosts" so here we should have
    the field of 'assigned' to this will helps us to avoid the contradition of 'two' argonosts
    test the same 'gathered info' ... so the logic behind here is that we should have the field
    which will be assigned when the 'argonists' takes the job.. here what i mean is that the
    'argrost' when he clicked the non-tested 'gathered' info he should have the button of 'Take Job'
    when he clicked that button he should have the 'job' assigned to him and this means will remove
    the 'job' from the list of non-assigned job... Here then i ask myself what if the
    'Argonist' takes the JOB fails to do? The answer behind this is every job assigned/taken by argonist
    should have the 'deadline' for it to be set free it can be maybe the 2 days if the test is not
    done then the job should be 'non-assigned' allowing for other or the same 'argonist' to do..... So
    here i need these fields.. 1. isAssigne(true, false), assignedTo(ArgoProfile1x1) ...
    assignedTo can be 'NULL' in case previous argo is no longer owner of job...
    or WHAT WE CAN DO IS TO NOT REMOVE Argonists WHEN THE JOB IS TAKEN FROM HIM BECAUSE WE HAVE THE isassigned
    field which determine if the job have somebody or not, is this value we can 'change' to indicate status and
    if isassigned is 'False' and we have 'assignedTo' user we can override him when another person is assigned the
    job... SO WHAT WE DEAL WITH HERE IS 'isassigned' field...
'''


'''
 the logic behind 'locked' and 'locked_at' field is to allow no contradiction between
 gatherman and argonomist.. because at the same time the 'argonomist' can be in the process
 of 'testing' and 'recommeding' the data while the 'gatherman' trying to change the data
 THIS WILL MAKE EITHER ARGONOMIST to test old data which will bring the 'contradiction' so
 TO AVOID THIS CASE WE SHOULD HAVE THE ARGONOMIST THE ABILITY TO 'LOCK' THE RECORDS FOR COUPLE
 OF DAY(FOR TESTING WE CAN MAKE IT ONE DAY) AND ALSO GIVE HIM HINT THAT AFTER COUPLE OF 'DAYS' OR
 TIME IF THE RECORDS IS NOT ALREADY TESTED OR RECOMMENDED IT BECAME 'UNLOCKED' BUT HE SHOULD FEEL FREE
 THAT TO LOCK AGAIN... COZ UKISEMA UMNYIME HUYU GATHERMAN ABILITY OF UPDATING DATA UNAKUA UNAKOSEA
 INABIDI TUMPE HIYO ABILITY KUWA UNAWEZA UKA-UPDATE DATA BAADAE IF THERE IS CHANGES... HII NI SCENARIO
 YA KWANZA .... VILEVILE
 UNAWEZA UKAAMUA UTOE SIKU ZA KUFANYA MAREKEBISHO KITU AMBACHO NAHISI NI SAHIHI KWA HII SCENARIO COZ SIKU
 HATA 3 ZINATOSHA KAMA HAMNA NO ANY CHANGES THEN DATA INAKUWA LOCKED KAMA WANAVYOFANYA GENIUS.. KO NAHISI
 TUENDE NA HII SCENARIO YA PILI KUWA WITHIN GIVEN PERIOD OF TIME BEFORE 'TESTING' YOU CAN UPDATE IT..
 nahisi HII NDO SEHEMU MUHIMU YA KUWEKA IS-LOCKED, SIONI KAMA KUNA ULAZIMA SANA WA KUWEKA KWA 'ARGONIST' COZ
 KWAKE KWA SASA SIO ISHU SANA...
'''


class SoilMetadata(models.Model):
    color = models.CharField(max_length=500, choices=SOIL_COLOR)
    temperature = models.IntegerField(
        help_text="Temperature is measured in Centigrades")
    structure = models.CharField(max_length=500, choices=SOIL_STRUCTURE)
    texture = models.CharField(max_length=500, choices=SOIL_TEXTURE)
    porosity = models.DecimalField(
        max_digits=3, decimal_places=2, help_text='Porosity is measured in g/cm**3')
    ph = models.DecimalField(
        max_digits=3, decimal_places=1, help_text="pH is decimal/number")
    form = models.CharField(max_length=200, choices=SOIL_FORM)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.color


class Farm(models.Model):
    current_use = models.TextField(
        help_text="Linatumika kufanyia nini kwa sasa")
    current_crop = models.TextField(
        help_text="Endapo mtu atasema linalimwa inabidi tujue ni zao gani", blank=True, null=True, max_length=8000)
    average_yield = models.TextField(
        help_text="Endapo linalimwa linatoa gunia ngapi", blank=True, null=True)
    # one farm should have one metadata.. one metadata should be associated with one farm
    farm_metadata = models.OneToOneField(
        GatheredInfo, on_delete=models.CASCADE, related_name="gatheredinfo")
    added_at = models.DateTimeField(auto_now_add=True)

    country = models.CharField(max_length=800, null=True, blank=True)
    region = models.CharField(max_length=800, null=True, blank=True)
    district = models.CharField(max_length=800, null=True, blank=True)
    ward = models.CharField(max_length=800, null=True, blank=True)
    street = models.CharField(max_length=800, null=True, blank=True)
    size = models.CharField(
        max_length=800, help_text="Size in hectras", null=True, blank=True)

    def __str__(self):
        return str(self.id)
    # soil = models.OneToOneField(
    #     SoilMetadata, on_delete=models.CASCADE, related_name="smetadata")

    @property
    def farm_location(self):
        return self.region + ', ' + self.district

    @property
    def have_report(self):
        if self.report.all().count() > 0:
            # hata kama ni many na except in most case one farm one recomms..
            # if kama zitakuwepo zaidi ya moja we'll take only the latest one..
            if (self.report.all().last().is_completed_and_recommended):
                return True
        else:
            return False

    @property
    def get_added_year(self):
        return self.farm_metadata.added_on.year

    @property
    def farm_owner(self):
        if self.farm_metadata:
            # if there is metadata
            return self.farm_metadata.owner.full_name

        else:
            return ''

    @property
    def get_recommended_fertilizer(self):
        if self.report.all().count() > 0:
            if self.report.all().last().is_completed_and_recommended:
                fname = json.loads(
                    self.report.all().last().recommendation.fertilizer_name)
                print('fertilizer ', ", ".join(fname))
                return ", ".join(fname)

            else:
                return ''
        else:
            return ''

    @property
    def get_recommended_crops(self):
        if self.report.all().count() > 0:
            if self.report.all().last().is_completed_and_recommended:
                cname = json.loads(
                    self.report.all().last().recommendation.crop)
                return ", ".join(cname)

            else:
                return ""
        else:
            return ""

    @property
    def get_seed_amount(self):
        if self.report.all().count() > 0:
            if self.report.all().last().is_completed_and_recommended:
                seed = self.report.all().last().recommendation.seed_amonunt_per_size_of_farm_or_hectare
                return json.loads(seed)
            else:
                return ""
        else:
            return ""

    @property
    def get_fertilizer_amount(self):
        if self.report.all().count() > 0:
            if self.report.all().last().is_completed_and_recommended:
                famount = json.loads(
                    self.report.all().last().recommendation.amount_of_fertilizer)
                return famount

            else:
                return ''
        else:
            return ''

    @property
    def registered_date(self):
        date = self.farm_metadata.added_on
        return date.strftime('%d/%m/%Y')

    @property
    def pragrammed_farmsize(self):
        coordinates = self.farm_metadata.coordinates.allCoords
        '''[
            "-6.814567704671967, 39.29239130724118",
            "-6.814642941765376, 39.29232492256586",
            "-6.814650265729579, 39.292334310297726",
            "-6.8146815590299585, 39.29230748820668",
            "-6.814808063840463, 39.29244696308009",
            "-6.8147967449903595, 39.29245702136423",
            "-6.814885298340722, 39.292556263099286",
            "-6.814789421029159, 39.29264209379061",
            "-6.814567704671967, 39.29239130724118"
           ]
        '''
        coords = []
        coordinates = json.loads(coordinates)
        for coordinate in coordinates:
            latlong = coordinate.split(',')
            latlong2 = []
            for element in latlong:
                latlong2.append(float(element))
            coords.append(latlong2)

        print(coords)
        # look like [[a,b], [c, d]]
        co = {
            'type': 'Polygon',
            'coordinates': [coords]
        }
        
        # area in meter square.
        return area(co)

    @property
    def farm_coordinates(self):
        coordinates = self.farm_metadata.coordinates.allCoords
        return json.loads(coordinates)

    # sitaki if nita-mdelete argonomic nataka report yake ibaki au sio... so on_delete=SET_NULL

    # https://eos.com/blog/soil-testing/


class TestResult(models.Model):
    sample_id = models.CharField(max_length=50, blank=True, null=True)
    soil_color = models.CharField(max_length=200, blank=True, null=True)
    soil_temperature = models.IntegerField(
        help_text="Temperature is measured in Centigrades", blank=True, null=True)
    soil_structure = models.CharField(max_length=500, blank=True, null=True)
    soil_texture = models.CharField(max_length=500, blank=True, null=True)
    soil_porosity = models.CharField(
        max_length=500, help_text='Porosity is measured in kg/m**3', blank=True, null=True)
    soil_ph = models.CharField(
        max_length=500, help_text="pH is decimal/number", blank=True, null=True)
    soil_form = models.CharField(max_length=200, blank=True, null=True)
    bulk_density = models.CharField(
        help_text="Bulk density we measure in kg/m3", max_length=500, blank=True, null=True)
    # https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjJ7vDj9r_9AhWrQaQEHdA8CNAQFnoECA8QAw&url=https%3A%2F%2Fsoilsensor.com%2Fsoil%2Fsoil-moisture-and-irrigation%2F&usg=AOvVaw087UP6LJflL0fpU097O82n
    soil_moisture = models.CharField(max_length=500,
                                     help_text="measured in water fraction by volute m3m-3", blank=True, null=True)
    phosphorus_level = models.CharField(max_length=500,
                                        help_text="measured in ppm-parts per millions", blank=True, null=True)
    potassium_level = models.CharField(max_length=500,
                                       help_text="measured in ppm-parts per millions", blank=True, null=True)
    nitrogen_level = models.CharField(max_length=500,
                                      help_text="measured in ppm-parts per milliions", blank=True, null=True)
    organic_matter = models.CharField(max_length=500,
                                      help_text="measured in t/ha tonne per hectare", blank=True, null=True)

    def __str__(self):
        return self.soil_color


class Recommendations(models.Model):
    crop = models.CharField(max_length=200, null=True, blank=True)
    # season it can be winter, summmer, autoum etc
    season = models.CharField(max_length=200, null=True, blank=True)
    fertilizer_name = models.CharField(
        max_length=800, null=True, blank=True)
    amount_of_fertilizer = models.CharField(max_length=800,
                                            help_text="Ujazo wa mbolea unaohitajika kutumia", blank=True, null=True)
    # inabidi aseme sawa mbolea kiasi gani tunaweza tukatumia kwenye shamba hilo
    seed_amonunt_per_size_of_farm_or_hectare = models.CharField(
        max_length=800, null=True, blank=True)
    # either kilimo kinaweza kiwe cha kutegemea mvua au cha umwagiliaji
    cultivation_type = models.CharField(
        max_length=800, null=True, blank=True)
    standard_yield = models.CharField(
        help_text="Unaweza ukapata magunia mangapi ukifata ushauri wake tunatumia magunia haya makubwa ya kilo 120", max_length=900, null=True, blank=True)
    brief_explanation = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.crop

    @property
    def get_farm_region(self):
        return self.fullreport.farm.region

    @property
    def get_farm_district(self):
        print()
        return self.fullreport.farm.district

    @property
    def get_report_date(self):
        return self.fullreport.added_on.year


class ArgoReport(models.Model):
    argonomist = models.ForeignKey(
        ArgonProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="argoreport")
    sampleId = models.CharField(max_length=300, null=True, blank=True)
    test_results = models.OneToOneField(
        TestResult, on_delete=models.CASCADE, related_name="testresults")
    # one farm can be associated with many reports..
    '''
        Hivi unajua foreign key inavyokuwa.. hii leo ndo mwisho usiludie tena yaani hap kwa mfano umeona hiii
        ArgoReport to Farm is ForeignKey this means the ArgoReport can be many for one report, na ndo maana
        nikifanya report.farm.all() inakuletea "error' that there is no all() attr in this..
        but nikifanya in reverse way farm.report.all() inakubali that means one Farm can have many report but 
        one farm to report.. this scenario you should understand, we'll fix at the letter but you should get that
        Foreign key means 'one'(model) to 'many'(reverse) which means the 'reverse' model can have many forward model
        while 'forward model' should contain only one 'reverse' model.. this should go in ur head. one to many means
        on accessing other model which in forward query mean it should have only one instance while in reverse 
        should have many.. Maybe u should ask is there is no ManyToOne???? which will succeed our condition here..
        Ikinisumbua naweza nikaibadilisha kwenda in ManyToMany
            farm = models.ManyToMany(Farm, blank=True, related_name="report")

        SEMA LOGIC YAKE HAPA KUELEWA NI EASY SANA IT MEANS THE REPORT CAN ACCESS ONLY ONE FARM, BUT FARM CAN ACCESS
        ALL REPORTS.. I THINK IT BASED IN THIS SCENARIO... BUT I THINK IN REVERSE YOU CAN ADD AS MANY AS FORWARD MODEL
        YOU WANT THAT'S IS HOW IT WORK.. SO FROM ONE FARM YOU CAN ADD MANY REPORTS ASSOCIATED WITH IT NA NDO KITU ALICHOTAKA
        HABIBU KUWA SHAMBA MOJA LINAWEZA LIKAWA TESTED HATA MARA 3 KWA MIAKA TOFAUTITOFAUTI..
    '''
    farm = models.ForeignKey(
        Farm, on_delete=models.SET_NULL, null=True, blank=True, related_name="report")
    # We should not user 'auto_now_add=True here since we want this value to only been created when instance is initially created...
    # so we should add this value when we initially save data to DB
    # https://stackoverflow.com/questions/7465796/django-set-datetimefield-to-database-servers-current-time
    added_on = models.DateTimeField()
    # hapa ndo inabidi tutumie auto_now_add=True since it update the 'date' everytime the instance is saved to the DB
    updated_at = models.DateTimeField(
        auto_now_add=True)
    recommendation = models.OneToOneField(
        Recommendations, on_delete=models.SET_NULL, null=True, blank=True, related_name="fullreport")
    # this check if the data is saved as complete but no recommendation given since we need to show some of our AI recommendation for argonomist to get more and provide accurate recommedation ...  IN THIS IF TRUE THEN THE ARGONOMIST CAN EDIT THE RECOMMENDATION AND OTHER TESTS.
    is_completed = models.BooleanField(default=False)
    # IN THIS WAY IF SAVED MEANS TEST COMPLETED AND RECOMMENDATION IS ALREADY PROVIDED, AT THIS STAGE THE ARGONOMIST CAN'T RECOMMEND AGAIN.. INFO WILL BE LOCKED AND MARKED COMPLETED..
    is_completed_and_recommended = models.BooleanField(default=False)
    # for now don't add the logic of locked and so on since Habibu will come and need you to change sth..
    # OLD NOT USEFUL NOW...

    def __str__(self):
        return self.argonomist.first_name + self.argonomist.last_name


class Soil(models.Model):
    color = models.CharField(max_length=500, choices=SOIL_COLOR)
    temperature = models.IntegerField(
        help_text="Temperature is measured in Centigrades")
    structure = models.CharField(max_length=500, choices=SOIL_STRUCTURE)
    texture = models.CharField(max_length=500, choices=SOIL_TEXTURE)
    # porosity = models.DecimalField(
    #     max_digits=3, decimal_places=2, help_text='Porosity is measured in g/cm**3')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.color


# OLD --- NOT USEFUL NOW...
class Shamba(models.Model):
    location = models.CharField(max_length=500)
    size = models.CharField(max_length=500)
    soil = models.OneToOneField(
        Soil, on_delete=models.CASCADE, unique=True, related_name='soil')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.location

# OLD NOT USEFUL NOW....


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, unique=True, related_name='mkulima')
    full_name = models.CharField(
        verbose_name='Full_name', max_length=500, default="#49DIE382OZ")
    profile_picture = models.ImageField(
        verbose_name="Avatar", upload_to='images/', default='images/profile.png')
    shamba = models.ManyToManyField(
        Shamba, blank=True, related_name="shamba")
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_profile(self):
        return self.profile_picture.url

    def __str__(self):
        return self.full_name


# Create your models here.
class regions(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(
        auto_now_add=True)
    updated_at = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):
        return self.name


class districts(models.Model):
    name = models.CharField(max_length=50)
    region_id = models.ForeignKey(regions, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    @property
    def region(self):
        return self.region_id.name

    def __str__(self):
        return self.name


class wards(models.Model):
    name = models.CharField(max_length=50)
    district_id = models.ForeignKey(districts, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    @ property
    def district(self):
        return self.district_id.name

    def __str__(self):
        return self.name
