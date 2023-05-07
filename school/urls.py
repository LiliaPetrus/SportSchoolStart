from django.contrib import admin
from django.urls import path
from rest_framework import routers

from . import views, api_views

router = routers.DefaultRouter()
router.register(r'sportsmans', api_views.SportsmanModelViewSet)
router.register(r'sections', api_views.SectionModelViewSet)
router.register(r'enrollments', api_views.EnrollmentRequestModelViewSet)

urlpatterns = router.urls
