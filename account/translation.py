from modeltranslation.translator import register, TranslationOptions

from account.models import UserInterestsFirst, UserInterestsSecond, UserInterestsThird, BeforeUniversity, University, \
    Course, Student, StudentCV, GroupStudent, Project, Comment, TestTask, AnswerTestTask, TaskGroup, AnswerGroup, \
    TaskStatusGroup, TaskStudent, TaskStatusStudent, DataKnowledgeFree, Chapter, UnderSection, DataKnowledge, Mailing, \
    StudentPortfolio


@register(UserInterestsFirst)
class UserInterestsFirstTranslationOptions(TranslationOptions):
    fields = ('interest',)


@register(UserInterestsSecond)
class UserInterestsSecondTranslationOptions(TranslationOptions):
    fields = ('interest',)


@register(UserInterestsThird)
class UserInterestsThirdTranslationOptions(TranslationOptions):
    fields = ('interest',)


@register(BeforeUniversity)
class BeforeUniversityTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(University)
class UniversityTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Student)
class StudentTranslationOptions(TranslationOptions):
    fields = ('full_name', 'mobile_phone', 'email', 'tg_nickname', 'age',
              'gender', 'before_university', 'university', 'faculty', 'course', 'interest_first',
              'other_interest_first',
              'interest_second', 'other_interest_second',
              'interest_third', 'other_interest_third', 'manager_status',
              'education_status', 'hours_per_week')


@register(StudentCV)
class StudentCVTranslationOptions(TranslationOptions):
    fields = ('student', 'file', 'create_date')


@register(GroupStudent)
class GroupStudentTranslationOptions(TranslationOptions):
    fields = ('name', 'captain', 'students', 'create_date')


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('group', 'name', 'intricacy', 'start_date', 'end_date')


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('project', 'user', 'student', 'comment_text', 'created_at',)


@register(TestTask)
class TestTaskTranslationOptions(TranslationOptions):
    fields = ('description', 'project_cost', 'start_date', 'end_date', 'grade',)


@register(AnswerTestTask)
class AnswerTestTaskTranslationOptions(TranslationOptions):
    fields = ('file', 'url', 'answer', 'user',)


@register(TaskGroup)
class AnswerTestTaskTranslationOptions(TranslationOptions):
    fields = ('project', 'description', 'project_cost', 'start_date', 'end_date', 'grade')


@register(AnswerGroup)
class AnswerGroupTaskTranslationOptions(TranslationOptions):
    fields = ('file', 'url', 'answer', 'user')


@register(TaskStatusGroup)
class TaskStatusGroupTranslationOptions(TranslationOptions):
    fields = ('task_group', 'date_create', 'status')


@register(TaskStudent)
class TaskStudentTranslationOptions(TranslationOptions):
    fields = ('project', 'student', 'description', 'project_cost', 'start_date', 'end_date', 'rating')


@register(TaskStatusStudent)
class TaskStatusStudentTranslationOptions(TranslationOptions):
    fields = ('task_student', 'date_create', 'status')


@register(DataKnowledgeFree)
class DataKnowledgeFreeTranslationOptions(TranslationOptions):
    fields = ('chapter', 'under_section', 'title', 'url',)


@register(Chapter)
class ChapterTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(UnderSection)
class ChapterTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(DataKnowledge)
class ChapterTranslationOptions(TranslationOptions):
    fields = ('chapter', 'under_section', 'title', 'url',)


@register(Mailing)
class MailingTranslationOptions(TranslationOptions):
    fields = ('subject', 'title', 'message', 'photo', 'sent_date', 'student',)


@register(StudentPortfolio)
class StudentPortfolioTranslationOptions(TranslationOptions):
    fields = ('student', 'file', 'create_date',)
