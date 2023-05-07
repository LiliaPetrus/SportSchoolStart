from rest_framework import viewsets

from . import models
from . import serializers


class SportsmanModelViewSet(viewsets.ModelViewSet):
    queryset = models.Sportsman.objects.all()
    serializer_class = serializers.SportsmanSerializer


class SectionModelViewSet(viewsets.ModelViewSet):
    queryset = models.Section.objects.all()
    serializer_class = serializers.SectionSerializer


class EnrollmentRequestModelViewSet(viewsets.ModelViewSet):
    queryset = models.EnrollmentRequest.objects.all()
    serializer_class = serializers.EnrollmentSerializer
