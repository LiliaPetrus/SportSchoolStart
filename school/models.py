from django.db import models
from datetime import date


MALE = 'm'
FEMALE = 'f'
EMPTY = ''

GENDER_CHOICE = [
    (EMPTY, 'не обрано'),
    (MALE, 'чол'),
    (FEMALE, 'жін'),
]

STATUS_EMPTY = 0
STATUS_NEW = 1
STATUS_ON_REVIEW = 2
STATUS_APPROVED = 3
STATUS_DENIED = 4


STATUS_CHOICE = (
    (STATUS_EMPTY, 'не обрано'),
    (STATUS_NEW, 'нова заявка'),
    (STATUS_ON_REVIEW, 'заявка на розгляді'),
    (STATUS_APPROVED, 'погоджено'),
    (STATUS_DENIED, 'відмовлено'),
)


def get_status_name(status_code: int) -> str:
    for s in STATUS_CHOICE:
        if status_code in s:
            return s[1]

    return ''


class Sportsman(models.Model):
    lastname = models.CharField(max_length=100, verbose_name='Прізвище')
    firstname = models.CharField(max_length=100, verbose_name='Ім\'я')
    patronymic = models.CharField(max_length=100, verbose_name='По батькові', blank=True, null=True)
    birthdate = models.DateField(verbose_name='Дата народження')
    gender = models.CharField(max_length=1, verbose_name='Стать', choices=GENDER_CHOICE, default=EMPTY)
    detail = models.TextField(verbose_name='Про спортсмена', blank=True, null=True)

    def __str__(self):
        return self.lastname + ' ' + self.firstname + ' ' + self.patronymic

    class Meta:
        verbose_name = 'Спортсмен'
        verbose_name_plural = 'Спортсмени'


class Section(models.Model):
    code = models.CharField(max_length=10, verbose_name='Код')
    name = models.CharField(max_length=100, verbose_name='Назва')
    age_from = models.SmallIntegerField(verbose_name='Вік з', blank=True, null=True)
    age_to = models.SmallIntegerField(verbose_name='Вік по', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Запис створено')
    all_places = models.SmallIntegerField(verbose_name='Кількість місць', default=0)
    free_places = models.SmallIntegerField(verbose_name='Вільних місць', default=0)
    description = models.TextField(verbose_name='Про секцію')

    def __update_free_places__(self):
        self.free_places = self.all_places - SectionSportsman.objects.filter(section_id=self.id).count()
        self.save()

    def __str__(self):
        return self.code + ' ' + self.name

    class Meta:
        verbose_name = 'Спортивна секція'
        verbose_name_plural = 'Спортивні секції'


class SectionSportsman(models.Model):
    section_id = models.ForeignKey(Section, on_delete=models.PROTECT)
    sportsman_id = models.ForeignKey(Sportsman, on_delete=models.PROTECT)
    date_start = models.DateField(verbose_name='Почав займатись з', blank=True, null=True)
    date_end = models.DateField(verbose_name='Закінчив займатись', blank=True, null=True)

    def __str__(self):
        return self.section_id.code + ' ' + self.section_id.name + ' ' + self.sportsman_id.lastname + ' ' + \
            date.strftime(self.sportsman_id.birthdate, '%d.%m.%Y')

    class Meta:
        verbose_name = 'Спортсмен секції'
        verbose_name_plural = 'Спортсмени секції'


class EnrollmentRequest(models.Model):
    section_id = models.ForeignKey(Section, on_delete=models.PROTECT)
    chat_id = models.PositiveIntegerField(verbose_name='chat id', default=0)
    lastname = models.CharField(max_length=100, verbose_name='Прізвище')
    firstname = models.CharField(max_length=100, verbose_name='Ім\'я')
    patronymic = models.CharField(max_length=100, verbose_name='По батькові', blank=True, null=True)
    birthdate = models.DateField(verbose_name='Дата народження')
    gender = models.CharField(max_length=1, verbose_name='Стать', choices=GENDER_CHOICE, default=EMPTY)
    status = models.SmallIntegerField(verbose_name='Статус заявки', choices=STATUS_CHOICE, default=STATUS_EMPTY)

    def __str__(self):
        return self.lastname + ' ' + self.firstname + ' ' + self.section_id.code + ' ' + self.section_id.name + \
            ' ' + get_status_name(self.status)

    class Meta:
        verbose_name = 'Заявка на запис до секції'
        verbose_name_plural = 'Заявки на запис до секції'
