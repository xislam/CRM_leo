import django_filters

from root import settings
from .models import Student
from django.contrib import admin
from django.utils.translation import gettext as _


class StudentFilter(django_filters.FilterSet):
    interest_first = django_filters.CharFilter(field_name='interest_first__name', lookup_expr='icontains')
    other_interest_first = django_filters.CharFilter(field_name='other_interest_first', lookup_expr='icontains')

    interest_second = django_filters.CharFilter(field_name='interest_second__name', lookup_expr='icontains')
    other_interest_second = django_filters.CharFilter(field_name='other_interest_second', lookup_expr='icontains')

    interest_third = django_filters.CharFilter(field_name='interest_third__name', lookup_expr='icontains')
    other_interest_third = django_filters.CharFilter(field_name='other_interest_third', lookup_expr='icontains')

    class Meta:
        model = Student
        fields = {
            'university': ['exact'],
            'course': ['exact'],
            # Добавьте другие поля для фильтрации

            # Добавляем кастомные фильтры
            'interest_first': ['icontains'],
            'other_interest_first': ['icontains'],
            'interest_second': ['icontains'],
            'other_interest_second': ['icontains'],
            'interest_third': ['icontains'],
            'other_interest_third': ['icontains'],
        }


class LanguageFilter(admin.SimpleListFilter):
    title = _('Language')
    parameter_name = 'language'

    def lookups(self, request, model_admin):
        return settings.ADMIN_LANGUAGE_REDIRECT_LANGUAGES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(language=self.value())
