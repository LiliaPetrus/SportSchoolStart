import datetime

from django.contrib import admin

from . import models


class SectionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'all_places', 'free_places')

    @staticmethod
    def get_free_places_count(obj) -> int:
        return obj.all_places - models.SectionSportsman.objects.filter(section_id=obj.id).count()

    def save_model(self, request, obj, form, change):
        obj.free_places = self.get_free_places_count(obj)
        super().save_model(request, obj, form, change)


class EnrollmentRequestAdmin(admin.ModelAdmin):
    @staticmethod
    def create_sportsman(obj) -> models.Sportsman:
        sportsman = models.Sportsman.objects.create(lastname=obj.lastname,
                                                    firstname=obj.firstname,
                                                    patronymic=obj.patronymic,
                                                    birthdate=obj.birthdate,
                                                    gender=obj.gender)
        sportsman.save()
        return sportsman

    @staticmethod
    def create_section_sportsman(obj, sportsman):
        section_sportsman = models.SectionSportsman.objects.create(section_id=obj.section_id,
                                                                   sportsman_id=sportsman,
                                                                   date_start=datetime.date.today())
        section_sportsman.save()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.status == models.STATUS_APPROVED:
            sportsman = self.create_sportsman(obj)
            self.create_section_sportsman(obj=obj, sportsman=sportsman)
            models.Section.objects.get(id=obj.section_id_id).__update_free_places__()


admin.site.register(models.Sportsman)
admin.site.register(models.Section, SectionAdmin)
admin.site.register(models.SectionSportsman)
admin.site.register(models.EnrollmentRequest, EnrollmentRequestAdmin)
