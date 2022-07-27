import django_filters
from welcome.models import MedicineCardInstance
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta


class MciFilter(django_filters.FilterSet):

    time_range = [
        (None, '------'),
        (1, _('1 month')),
        (6, _('6 month')),
        (12, _('1 year')),
        (24, _('2 year')),
        (36, _('3 year')),
        (60, _('5 year')),
    ]

    date = django_filters.ChoiceFilter(label='Time range', choices=time_range, method='select_by_date')

    class Meta:
        model = MedicineCardInstance
        fields = ('doctors', 'medical_establishments', 'medical_field')

    def select_by_date (self, queryset, name, value):
        enddate = date.today()
        startdate = enddate - timedelta(days=float(value) * 30.4167)
        return queryset.filter(registration_at__range=[startdate, enddate])

