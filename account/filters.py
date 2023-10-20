import django_filters
from django.db.models import Q, Count

from root import settings
from .models import Student, UserInterestsThird, UserInterestsSecond, UserInterestsFirst
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


class InterestFirstFilter(admin.SimpleListFilter):
    title = 'Профессиональная сфера интересов'
    parameter_name = 'interest_first'

    def lookups(self, request, model_admin):
        interests = UserInterestsFirst.objects.all()
        return [(interest.id, interest.interest) for interest in interests]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                Q(interest_first__id=self.value()) | Q(other_interest_first=self.value())
            )


class InterestSecondFilter(admin.SimpleListFilter):
    title = 'Интересующие Вас ниши'
    parameter_name = 'interest_second'

    def lookups(self, request, model_admin):
        interests = UserInterestsSecond.objects.all()
        return [(interest.id, interest.interest) for interest in interests]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                Q(interest_second__id=self.value()) | Q(other_interest_second=self.value())
            )


class InterestThirdFilter(admin.SimpleListFilter):
    title = 'Цели'
    parameter_name = 'interest_third'

    def lookups(self, request, model_admin):
        interests = UserInterestsThird.objects.all()
        return [(interest.id, interest.interest) for interest in interests]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                Q(interest_third__id=self.value()) | Q(other_interest_third=self.value())
            )


# class ProjectsCountFilter(admin.SimpleListFilter):
#     title = _('Количество сделанных проектов')
#     parameter_name = 'projects_count'
#
#     def lookups(self, request, model_admin):
#         return (
#             ('1', _('1 проект')),
#             ('2', _('2 проекта')),
#             ('3', _('3 и более проектов')),
#         )
#
#     def queryset(self, request, queryset):
#         if self.value() == '1':
#             return queryset.annotate(projects_completed=Count('group__project')).filter(projects_completed=1)
#         if self.value() == '2':
#             return queryset.annotate(projects_completed=Count('group__project')).filter(projects_completed=2)
#         if self.value() == '3':
#             return queryset.annotate(projects_completed=Count('group__project')).filter(projects_completed__gte=3)
