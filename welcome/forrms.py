from django import forms
from django.forms import ModelForm
from welcome.models import *
from django.core.exceptions import ValidationError
from welcome.functions import check_file_type
from datetime import date
from django.utils.translation import gettext_lazy as _


def file_size(value):  # add this to some file where you can import it from
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(_('File too large. Size should not exceed 5 MB.'))
    if check_file_type(value.name)['type'] == 'dangerous':
        raise ValidationError(_('This file is not allowed.'))


def get_y():
    start_year = 1900
    BIRTH_YEAR_CHOICES = []
    while start_year <= int(date.today().year):
        BIRTH_YEAR_CHOICES.append(str(start_year))
        start_year = start_year + 1
    return BIRTH_YEAR_CHOICES


BIRTH_YEAR_CHOICES = get_y()
REVERSE_YEAR = list(reversed(BIRTH_YEAR_CHOICES))
FAVORITE_COLORS_CHOICES = [
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
]


class AddMedicineCardInstance(ModelForm):
    registration_at = forms.DateTimeField(
        label=_('Date of medical analysis'),
        widget=forms.SelectDateWidget(years=REVERSE_YEAR)
    )

    class Meta:
        model = MedicineCardInstance
        fields = ['title', 'registration_at', 'description', 'medical_establishments', 'doctors', 'medical_field']


class EditMedicineCardInstance(ModelForm):
    class Meta:
        model = MedicineCardInstance
        fields = ['title', 'registration_at', 'description', 'medical_establishments', 'doctors', 'medical_field']


class AddMedicineCard(ModelForm):
    user_birthday_date = forms.DateTimeField(
        label=_('Enter your date of birth'),
        widget=forms.SelectDateWidget(years=REVERSE_YEAR)
    )

    class Meta:
        model = MedicineCard
        fields = ['user_birthday_date']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddMedicineCard, self).__init__(*args, **kwargs)

class EditMedicineCard(ModelForm):
    user_birthday_date = forms.DateTimeField(
        label=_('Enter your date of birth'),
        widget=forms.SelectDateWidget(years=REVERSE_YEAR)
    )

    class Meta:
        model = MedicineCard
        fields = ['user_birthday_date']

class AddPrivateDocument(ModelForm):
    upload = forms.FileField(validators=[file_size])

    class Meta:
        model = PrivateDocument
        fields = ['upload']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.upload.u = Author.objects.filter(name__startswith='O')


class EditDoctorForm(ModelForm):
    class Meta:
        model = Doctors
        fields = ['name', 'phone_number']


class EditMedicalFieldForm(ModelForm):
    class Meta:
        model = MedicalField
        fields = ['name']


class EditMedicalEstablishmentForm(ModelForm):
    class Meta:
        model = MedicalEstablishments
        fields = ['name', 'address', 'phone_number', 'site']


class AddMedicalEstablishmentForm(ModelForm):

    class Meta:
        model = MedicalEstablishments
        fields = ['name', 'phone_number', 'address', 'site']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddMedicalEstablishmentForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        if MedicalEstablishments.objects.filter(user=self.user, name=name).exists():
            raise forms.ValidationError(_('You already have a medical facility with that name.'))
        return name


class AddDoctorForm(ModelForm):

    class Meta:
        model = Doctors
        fields = ['name', 'phone_number']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddDoctorForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        if Doctors.objects.filter(user=self.user, name=name).exists():
            raise forms.ValidationError(_('You already have a doctor with this name.'))
        return name


class AddMedicalField(ModelForm):

    class Meta:
        model = MedicalField
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddMedicalField, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        if MedicalField.objects.filter(user=self.user, name=name).exists():
            raise forms.ValidationError(_('You already have a field of medicine with that name'))
        return name
