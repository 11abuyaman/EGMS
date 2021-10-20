import django_filters
from django.db.models import Q

from services.models import User


class PatientsFilter(django_filters.FilterSet):
    patient_name = django_filters.CharFilter(lookup_expr='icontains', method='name_filter')
    national_number = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['patient_name', 'national_number']

    def name_filter(self, queryset, name, value):
        value = value.strip()
        if ' ' in value:
            value = value.split(' ')
            f_name = value[0]
            l_name = value[1]
            qs = queryset.filter(Q(first_name__icontains=f_name) & Q(last_name__icontains=l_name))
        else:
            qs = queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value))
        return qs
