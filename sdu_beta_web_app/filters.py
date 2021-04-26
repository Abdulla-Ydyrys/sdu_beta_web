import django_filters
from django.db.models import Q
from .models import *

class RegistrationFilter(django_filters.FilterSet):
    student_id = django_filters.CharFilter(field_name='student_id__student__username', lookup_expr='icontains')

    class Meta:
        model = Students_registration
        fields = '__all__'
        exclude = ['id', 'supervisor_id', 'agreement', 'reject_reason', 'created_at', 'updated_at', 'object']


class ReportFilter(django_filters.FilterSet):
    student_id = django_filters.CharFilter(field_name='student_id__student__first_name', lookup_expr='icontains')
    class Meta:
        model = Report_submitting
        fields = '__all__'
        exclude = ['id', 'report_id', 'references', 'grade', 'created_at', 'updated_at', 'object']

class StudentFilter(django_filters.FilterSet):
    student_id = django_filters.CharFilter(field_name='student_id__student__first_name', lookup_expr='icontains')
    class Meta:
        model = Students_registration
        fields = '__all__'
        exclude = ['id', 'supervisor_id', 'beta_type', 'agreement', 'registration_status', 'reject_reason', 'created_at', 'updated_at', 'object']