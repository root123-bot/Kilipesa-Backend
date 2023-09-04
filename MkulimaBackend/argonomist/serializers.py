
from rest_framework import serializers
from MkulimaBackend.mkulima.models import *


class ArgonomistSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArgonProfile
        fields = [
            'id',
            'full_name',
            'location',
            'profile',
            'tasks',
            'status',
            'phone'
        ]
