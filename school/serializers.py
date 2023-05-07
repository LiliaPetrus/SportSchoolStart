from rest_framework import serializers

from . import models


class SportsmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sportsman
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Section
        fields = '__all__'


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EnrollmentRequest
        fields = '__all__'


class SectionSportsmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SectionSportsman
        fields = '__all__'

