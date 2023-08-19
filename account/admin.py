from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.html import format_html
from django.urls import reverse

from account.models import User, Student, GroupStudent, StudentCV, StudentPortfolio, Project, Comment, TaskGroup, \
    TaskStudent, TaskStatusStudent, TaskStatusGroup, UserInterestsFirst, UserInterestsSecond, UserInterestsThird, \
    University, BeforeUniversity, Course, DataKnowledge, UnderSection, Chapter


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username', 'tg_nickname', 'full_name', 'mobile_phone', 'email', 'age', 'gender', 'university', 'course',
            'faculty')


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ('General', {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': (
                'full_name', 'email', 'mobile_phone', 'tg_nickname', 'age', 'gender', 'university', 'course', 'faculty')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_form = CustomUserCreationForm


admin.site.register(User, CustomUserAdmin)


class StudentCVInline(admin.TabularInline):
    model = StudentCV
    extra = 1  # Number of empty forms to display for adding new entries


class StudentPortfolioInline(admin.TabularInline):
    model = StudentPortfolio
    extra = 1  # Number of empty forms to display for adding new entries


class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'university', 'course', 'hours_per_week')
    list_filter = ('university', 'before_university', 'course',)
    search_fields = ('full_name', 'email', 'tg_nickname')
    inlines = [StudentCVInline, StudentPortfolioInline]


admin.site.register(Student, StudentAdmin)
admin.site.register(StudentCV)
admin.site.register(University)
admin.site.register(BeforeUniversity)

admin.site.register(StudentPortfolio)

admin.site.register(UserInterestsFirst)
admin.site.register(UserInterestsSecond)
admin.site.register(UserInterestsThird)
admin.site.register(Course)

admin.site.register(Chapter)
admin.site.register(UnderSection)
admin.site.register(DataKnowledge)


class ProjectInline(admin.TabularInline):
    model = Project.group.through
    extra = 1


class GroupAdmin(admin.ModelAdmin):
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


admin.site.register(GroupStudent, GroupAdmin)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class TaskGroupInline(admin.TabularInline):
    model = TaskGroup


class TaskStudentInline(admin.TabularInline):
    model = TaskStudent


class ProjectAdmin(admin.ModelAdmin):
    inlines = [CommentInline, TaskStudentInline, TaskGroupInline]


admin.site.register(Project, ProjectAdmin)


class TaskStatusStudentInline(admin.TabularInline):
    model = TaskStatusStudent
    extra = 1
    readonly_fields = ('date_create',)


class TaskStudentAdmin(admin.ModelAdmin):
    # ... other configurations ...

    # Add the TaskStatusStudentInline to the inlines list
    inlines = [TaskStatusStudentInline]


class TaskGroupStudentInline(admin.TabularInline):
    model = TaskStatusGroup
    extra = 1
    readonly_fields = ('date_create',)


class TaskGroupAdmin(admin.ModelAdmin):
    # ... other configurations ...

    # Add the TaskStatusStudentInline to the inlines list
    inlines = [TaskGroupStudentInline]


admin.site.register(TaskGroup, TaskGroupAdmin)
admin.site.register(TaskStudent, TaskStudentAdmin)
