import django_filters

from root import settings
from .models import Student
from django.contrib import admin
from django.utils.translation import gettext as _


class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = {
            'university': ['exact'],
            'course': ['exact'],
            # Добавьте другие поля для фильтрации
        }


class LanguageFilter(admin.SimpleListFilter):
    title = _('Language')
    parameter_name = 'language'

    def lookups(self, request, model_admin):
        return settings.ADMIN_LANGUAGE_REDIRECT_LANGUAGES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(language=self.value())
