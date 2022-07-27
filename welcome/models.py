from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from medical_card.storage_backends import PrivateMediaStorage
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone


# Функция формирует путь для документов которые сохраняются
def upload_path_handler(instance, filename):
    return "user_{id}/{file}".format(id=instance.mci.medicine_card.user.username, file=filename)


# Функиця валидатор даты рождения, дату рождения на реалистичность.
def validate_even(value):
    today = date.today()
    var = today.year - value.year - (
            (today.month, today.day) < (value.month, value.day))
    if var > 130:
        raise ValidationError(
            _('%(value)s Not realistic date of birth'),
            params={'value': value},
        )
    if date.today() < value:
        raise ValidationError(
            _('%(value)s Date of birth is in the future'),
            params={'value': value},
        )


class MedicalEstablishments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Название лечебного учреждения')
    address = models.CharField(max_length=80, default=None, null=True, blank=True,
                               verbose_name='Адрес лечебного учреждения')
    phone_number = models.CharField(max_length=20, default=None, null=True, blank=True,
                                    verbose_name='Телефон лечебного учреждения')
    site = models.CharField(max_length=255, default=None, null=True, blank=True,
                            verbose_name='Сайт лечебного учреждения')

    def __str__(self):
        return str(self.name)


class Doctors(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Имя и фамилия врача')
    phone_number = models.CharField(max_length=20, default=None, null=True, blank=True, verbose_name='Номер телефона')

    def __str__(self):
        return str(self.name)


    # def get_absolute_url(self):
    #     return reverse('add-doctor', kwargs={'pk': self.pk})


class MedicalField(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Пожалуйста добавьте область медицины')

    def __str__(self):
        return str(self.name)


class MedicineCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_birthday_date = models.DateField(validators=[validate_even], verbose_name='Укажите вашу дату рождения')
    registration_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class MedicineCardInstance(models.Model):
    medicine_card = models.ForeignKey(MedicineCard, on_delete=models.CASCADE)
    registration_at = models.DateField(verbose_name='Дата проведения исследования')
    title = models.CharField(max_length=50, null=True, blank=True, default=None, verbose_name='Краткое описание записи')
    description = models.TextField(max_length=1000, null=False, blank=True, default=None, verbose_name='Полное описание записи')
    p_age = models.SmallIntegerField(default=1,
                                     verbose_name='Количество полных лет пациента на момент проведения исследования')
    p_age_status = models.BooleanField(default=False)
    medical_establishments = models.ForeignKey(
        MedicalEstablishments,
        blank=True,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Лечебное учреждение'
    )
    doctors = models.ForeignKey(
        Doctors,
        blank=True,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Лечащий врач'
    )
    medical_field = models.ForeignKey(
        MedicalField,
        blank=True,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Область медицины'
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ('-registration_at',)




class PrivateDocument(models.Model):
    mci = models.ForeignKey(MedicineCardInstance, on_delete=models.CASCADE)
    uploaded_at = models.DateField(auto_now_add=True)
    upload = models.FileField(storage=PrivateMediaStorage(), upload_to=upload_path_handler,
                              verbose_name='Загрузить документ')


# Обработчик сигнала пост сейв модели MedicineCardInstance. Рассчитывает сколько полных лет было пациенту на момент
# исследования и сохраняет значение в модель
@receiver(post_save, sender=MedicineCardInstance)
def edit_p_age(sender, **kwargs):
    mci = MedicineCardInstance.objects.get(pk=kwargs['instance'].pk)
    if not mci.p_age_status:
        user_birthday_date = mci.medicine_card.user_birthday_date
        mci_data = mci.registration_at
        age = mci_data.year - user_birthday_date.year - (
                    (mci_data.month, mci_data.day) < (user_birthday_date.month, user_birthday_date.day))
        mci.p_age = int(age)
        mci.p_age_status = True
        mci.save()

