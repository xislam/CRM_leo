from django import forms
from django.utils.translation import gettext_lazy as _
from modeltranslation.forms import TranslationModelForm
from account.models import University, Course, BeforeUniversity, Mailing, UserInterestsFirst, UserInterestsSecond, \
    UserInterestsThird, Student, StudentCV, StudentPortfolio, GroupStudent, Project, Comment, TestTask, AnswerTestTask, \
    TaskGroup, AnswerGroup, TaskStatusGroup, TaskStudent, AnswersStudent, TaskStatusStudent, DataKnowledgeFree, Chapter, \
    UnderSection, DataKnowledge


class StudentFilterForm(forms.Form):
    MANAGER_STATUSES = [
        ('', _('Все')),
        ('lead', _('Лид')),
        ('in_progress', _('В работе у менеджера')),
        ('rejected', _('Отказ')),
        ('waiting_for_payment', _('Ожидает оплаты')),
        ('partially_paid', _('Частично оплачен')),
        ('paid', _('Оплачен')),
    ]

    EDUCATION_STATUSES = [
        ('', _('Все')),
        ('free_subscription_registration', _('Регистрация на бесплатную подписку')),
        ('completed_free_subscription', _('Завершена бесплатная подписка')),
        ('paid_subscription_member', _('Участник платной подписки')),
        ('course_participant', _('Участник курса')),
        ('dropped_out', _('Выбыл')),
        ('completed_education', _('Завершил обучение')),
    ]

    before_university = forms.ModelChoiceField(queryset=BeforeUniversity.objects.all(), empty_label=_("Образование"),
                                               widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    university = forms.ModelChoiceField(queryset=University.objects.all(), empty_label=_("Все университеты"),
                                        widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label=_("Все курсы"),
                                    widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    manager_status = forms.ChoiceField(choices=MANAGER_STATUSES, required=False,
                                       widget=forms.Select(attrs={'class': 'form-control'}))

    education_status = forms.ChoiceField(choices=EDUCATION_STATUSES, required=False,
                                         widget=forms.Select(attrs={'class': 'form-control'}))


class MailingForm(forms.ModelForm):
    subject = forms.CharField(label=False,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Тема')}))
    title = forms.CharField(label=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Заголовок')}))
    message = forms.CharField(label=False,
                              widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('Сообщение')}))
    photo = forms.ImageField(label=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                             required=False)

    class Meta:
        model = Mailing
        fields = ['subject', 'title', 'message', 'photo']


class UserInterestsFirstForm(TranslationModelForm):
    class Meta:
        model = UserInterestsFirst
        fields = ('interest',)


class UserInterestsSecondForm(TranslationModelForm):
    class Meta:
        model = UserInterestsSecond
        fields = ('interest',)


class UserInterestsThirdForm(TranslationModelForm):
    class Meta:
        model = UserInterestsThird
        fields = ('interest',)


class BeforeUniversityForm(TranslationModelForm):
    class Meta:
        model = BeforeUniversity
        fields = ('name',)


class UniversityForm(TranslationModelForm):
    class Meta:
        model = University
        fields = ('name',)


class CourseForm(TranslationModelForm):
    class Meta:
        model = Course
        fields = ('name',)


class StudentForm(TranslationModelForm):
    class Meta:
        model = Student
        fields = ('full_name', 'mobile_phone', 'email', 'tg_nickname', 'age', 'gender', 'before_university',
                  'university', 'faculty', 'course', 'interest_first', 'other_interest_first', 'interest_second',
                  'other_interest_second', 'interest_third', 'other_interest_third', 'manager_status',
                  'education_status', 'hours_per_week', 'projects','telegram_user_id')


class StudentCVForm(TranslationModelForm):
    class Meta:
        model = StudentCV
        fields = ('student', 'file')


class StudentPortfolioForm(TranslationModelForm):
    class Meta:
        model = StudentPortfolio
        fields = ('student', 'file')


class GroupStudentForm(TranslationModelForm):
    class Meta:
        model = GroupStudent
        fields = ('name', 'captain', 'students')


class ProjectForm(TranslationModelForm):
    class Meta:
        model = Project
        fields = ('group', 'name', 'intricacy', 'start_date', 'end_date', 'group_grade', 'intricacy_coefficient')


class CommentForm(TranslationModelForm):
    class Meta:
        model = Comment
        fields = ('project', 'user', 'student', 'comment_text')


class TestTaskForm(TranslationModelForm):
    class Meta:
        model = TestTask
        fields = ('description', 'project_cost', 'start_date', 'end_date', 'grade')


class AnswerTestTaskForm(TranslationModelForm):
    class Meta:
        model = AnswerTestTask
        fields = ('file', 'url', 'answer', 'user')


class TaskGroupForm(TranslationModelForm):
    class Meta:
        model = TaskGroup
        fields = ('project', 'description', 'project_cost', 'start_date', 'end_date', 'grade')


class AnswerGroupForm(TranslationModelForm):
    class Meta:
        model = AnswerGroup
        fields = ('file', 'url', 'answer', 'user')


class TaskStatusGroupForm(TranslationModelForm):
    class Meta:
        model = TaskStatusGroup
        fields = ('task_group', 'status')


class TaskStudentForm(TranslationModelForm):
    class Meta:
        model = TaskStudent
        fields = ('project', 'student', 'description', 'project_cost', 'start_date', 'end_date',  'personal_grade',
                  'deadline_compliance', 'manager_recommendation')


class AnswersStudentForm(TranslationModelForm):
    class Meta:
        model = AnswersStudent
        fields = ('file', 'url', 'answer', 'user',)


class TaskStatusStudentForm(TranslationModelForm):
    class Meta:
        model = TaskStatusStudent
        fields = ('task_student', 'status')


class DataKnowledgeFreeForm(TranslationModelForm):
    class Meta:
        model = DataKnowledgeFree
        fields = ('chapter', 'under_section', 'title', 'url', 'files')


class DataKnowledgeForm(TranslationModelForm):
    class Meta:
        model = DataKnowledge
        fields = ('chapter', 'under_section', 'title', 'url', 'files')


class ChapterForm(TranslationModelForm):
    class Meta:
        model = Chapter
        fields = ('name',)


class UnderSectionForm(TranslationModelForm):
    class Meta:
        model = UnderSection
        fields = ('name',)


class MailingTranslationForm(TranslationModelForm):
    class Meta:
        model = Mailing
        fields = ('subject', 'title', 'message', 'photo', 'student')
