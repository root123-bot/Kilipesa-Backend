from rest_framework import serializers
from .models import *

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = [
            'email'
        ]

class GatheredInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatheredInfo
        fields = [
            'id',
            'added_on',
            'farm_owner',
            'farm',
            'get_coordinates',
            'farm_location',
            'nextkin_info',
            'get_owner_info',
            'family_details',
        ]

class GathermanSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatherProfile
        fields = [
            'id',
            'full_name',
            'phone',
            'profile_pic',
            'location',
            'ward',
            'number_of_records',
            'recordsaddedtoday',
            'profileIsCompleted',
            "education_level"
        ]


class FarmOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = [
            'id',
            'full_name',
            'phone',
            'age',
            'profile_pic',
            'noOfFarms',
            'totalSize',
            'location',
            # 'family_details',
        ]

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendations
        fields = [
            'id',
            'crop',
            'fertilizer_name',
            'standard_yield',
            'get_farm_region',
            'get_farm_district',
            'get_report_date',
        ]


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = [
            'id',
            'have_report',
            'farm_owner',
            'get_recommended_fertilizer',
            'get_recommended_crops',
            'size',
            'farm_location',
            'region',
            'district',
            'get_added_year',
            'get_seed_amount',
            'get_fertilizer_amount',
            'registered_date',
            'farm_coordinates',
            'pragrammed_farmsize',
        ]


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'full_name',
            'get_profile'
        ]


class RegionSerializers(serializers.ModelSerializer):
    class Meta:
        model = regions
        fields = [
            'id',
            'name'
        ]


class DistrictSerializers(serializers.ModelSerializer):
    class Meta:
        model = districts
        fields = [
            'id',
            'name',
            'region',
        ]


class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = regions
        fields = [
            'id',
            'name'
        ]
