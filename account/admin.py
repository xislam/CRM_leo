from django.contrib import admin, messages
from django.contrib.admin import TabularInline
from django.db.models import Q, Count
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from django import forms

from account.filters import InterestFirstFilter, InterestSecondFilter, InterestThirdFilter
from account.forms import UserInterestsFirstForm, StudentForm, UserInterestsSecondForm, UserInterestsThirdForm, \
    GroupStudentForm, CourseForm, StudentCVForm, UniversityForm, BeforeUniversityForm, StudentPortfolioForm, \
    ChapterForm, UnderSectionForm, DataKnowledgeForm, DataKnowledgeFreeForm, TaskGroupForm, TaskStudentForm, \
    TestTaskForm, AnswersStudentForm, TaskStatusStudentForm, CommentForm, TaskStatusGroupForm, AnswerGroupForm, \
    MailingTranslationForm, ProjectForm, AnswerTestTaskForm
from account.models import Student, GroupStudent, StudentCV, StudentPortfolio, Project, Comment, TaskGroup, \
    TaskStudent, TaskStatusStudent, TaskStatusGroup, UserInterestsFirst, UserInterestsSecond, UserInterestsThird, \
    University, BeforeUniversity, Course, DataKnowledge, UnderSection, Chapter, Mailing, AnswerGroup, AnswersStudent, \
    AnswerTestTask, TestTask, DataKnowledgeFree


class StudentCVInline(TabularInline):
    model = StudentCV
    extra = 1  # Number of empty forms to display for adding new entries
    fk_name = 'student'
    form = StudentCVForm


class StudentPortfolioInline(TabularInline):
    model = StudentPortfolio
    extra = 1  # Number of empty forms to display for adding new entries
    form = StudentPortfolioForm
    fk_name = 'student'


class MailingSelectionForm(forms.Form):
    mailing = forms.ModelChoiceField(
        queryset=Mailing.objects.all(),
        empty_label=None,  # Чтобы не было пустой опции
        widget=forms.Select(attrs={'class': 'form-control'})
    )

from django.contrib import admin
from .models import Student
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    list_display = ('full_name', 'university', 'course', 'hours_per_week', 'total_rating', 'projects_count')
    list_filter = ('university', 'before_university', 'course', InterestFirstFilter, InterestSecondFilter, InterestThirdFilter)
    search_fields = ('full_name', 'email', 'tg_nickname')
    actions = ['send_custom_email']
    inlines = [StudentCVInline, StudentPortfolioInline]
    ordering = ('-total_rating',)


    def total_rating(self, obj):
        return obj.calculate_total_rating()

    total_rating.short_description = 'Общий рейтинг'

    def projects_count(self, obj):
        return obj.projects_in_group()

    projects_count.short_description = 'Количество проектов в группе'


@admin.register(StudentCV)
class StudentCVAdmin(admin.ModelAdmin):
    form = StudentCVForm


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    form = UniversityForm


@admin.register(BeforeUniversity)
class BeforeUniversityAdmin(admin.ModelAdmin):
    form = BeforeUniversityForm


@admin.register(StudentPortfolio)
class StudentPortfolioAdmin(admin.ModelAdmin):
    form = StudentPortfolioForm


@admin.register(UserInterestsFirst)
class UserInterestsFirstAdmin(admin.ModelAdmin):
    form = UserInterestsFirstForm


@admin.register(UserInterestsSecond)
class UserInterestsSecondAdmin(admin.ModelAdmin):
    form = UserInterestsSecondForm


@admin.register(UserInterestsThird)
class UserInterestsThirdAdmin(admin.ModelAdmin):
    form = UserInterestsThirdForm


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    form = CourseForm


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    form = ChapterForm


@admin.register(UnderSection)
class UnderSectionAdmin(admin.ModelAdmin):
    form = UnderSectionForm


@admin.register(DataKnowledge)
class DataKnowledgeAdmin(admin.ModelAdmin):
    form = DataKnowledgeForm


@admin.register(DataKnowledgeFree)
class DataKnowledgeFreeAdmin(admin.ModelAdmin):
    form = DataKnowledgeFreeForm


class ProjectInline(TabularInline):
    model = Project.group.through
    extra = 1
    verbose_name = _('Проект')
    verbose_name_plural = _('Проект')


@admin.register(GroupStudent)
class GroupAdmin(admin.ModelAdmin):
    form = GroupStudentForm
    list_display = ('name', 'get_students_table')
    list_filter = (
        'students__university', 'students__course')  # Используем связанные поля из модели Student

    def get_students_table(self, obj):
        # Создаем таблицу с данными о студентах
        table_html = "<table>"
        table_html += "<tr><th>ФИО</th><th>Мобильный телефон</th><th>Электронная почта</th><th>Ник в Телеграм</th><th>Возраст</th><th>Пол</th><th>ВУЗ</th><th>Курс</th><th>Факультет</th><th>Статус</th><th>Часов в неделю</th></tr>"
        for student in obj.students.all():
            edit_url = reverse('admin:%s_%s_change' % (student._meta.app_label, student._meta.model_name),
                               args=[student.pk])
            table_html += f"<tr><td><a href='{edit_url}'>{student.full_name}</a></td><td>{student.mobile_phone}</td><td>{student.email}</td><td>{student.tg_nickname}</td><td>{student.age}</td><td>{student.gender}</td><td>{student.university}</td><td>{student.course}</td><td>{student.faculty}</td><td></td><td>{student.hours_per_week}</td></tr>"
        table_html += "</table>"
        return format_html(table_html)

    get_students_table.short_description = 'Студенты'
    inlines = [ProjectInline]


class CommentInline(TabularInline):
    model = Comment
    extra = 1
    form = CommentForm
    fk_name = 'project'


class TaskGroupInline(TabularInline):
    model = TaskGroup
    form = TaskGroupForm
    fk_name = 'project'


class TaskStudentInline(TabularInline):
    model = TaskStudent
    form = TaskStudentForm
    fk_name = 'project'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    inlines = [CommentInline, TaskStudentInline, TaskGroupInline]
    readonly_fields = ('grade',)


class TaskStatusStudentInline(TabularInline):
    model = TaskStatusStudent
    form = TaskStatusStudentForm
    extra = 1
    fk_name = 'task_student'


class AnswersStudentInline(TabularInline):
    model = AnswersStudent
    form = AnswersStudentForm
    extra = 1


@admin.register(TaskStudent)
class TaskStudentAdmin(admin.ModelAdmin):
    # ... other configurations ..
    form = TaskStudentForm
    # Add the TaskStatusStudentInline to the inlines list
    inlines = [TaskStatusStudentInline, AnswersStudentInline]


class TaskGroupStudentInline(TabularInline):
    model = TaskStatusGroup
    extra = 1
    form = TaskStatusGroupForm
    fk_name = 'task_group'


class AnswerGroupInline(TabularInline):
    model = AnswerGroup
    extra = 1
    form = AnswerGroupForm
    fk_name = 'answer'


@admin.register(TaskGroup)
class TaskGroupAdmin(admin.ModelAdmin):
    # ... other configurations ...
    form = TaskGroupForm
    # Add the TaskStatusStudentInline to the inlines list
    inlines = [TaskGroupStudentInline, AnswerGroupInline]


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    form = MailingTranslationForm


class AnswerAnswerGroupInline(TabularInline):
    model = AnswerTestTask
    extra = 1
    form = AnswerTestTaskForm
    fk_name = 'answer'


@admin.register(TestTask)
class TestTaskAdmin(admin.ModelAdmin):
    # ... other configurations ...
    form = TestTaskForm
    # Add the TaskStatusStudentInline to the inlines list
    inlines = [AnswerAnswerGroupInline]
