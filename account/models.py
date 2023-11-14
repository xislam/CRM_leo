from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.db.models import Max, Sum, Count, Avg
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from django import forms


# class CustomUserManager(BaseUserManager):
#     def create_user_without_password(self, tg_nickname, **extra_fields):
#         """
#         Создает и сохраняет пользователя с указанным tg_nickname, без установки пароля.
#         """
#         if not tg_nickname:
#             raise ValueError('У пользователя должен быть указан tg_nickname')
#
#         user = self.model(tg_nickname=tg_nickname, is_active=True, **extra_fields)
#         user.save(using=self._db)
#         return user


class UserInterestsFirst(models.Model):
    interest = models.CharField(verbose_name=_('Интерес'), max_length=150)

    def __str__(self):
        return self.interest

    class Meta:
        verbose_name = _('Профессиональная сфера интересов')
        verbose_name_plural = _('Профессиональная сфера интересов')


class UserInterestsSecond(models.Model):
    interest = models.CharField(verbose_name=_('Интерес'), max_length=150)

    def __str__(self):
        return self.interest

    class Meta:
        verbose_name = _('Интересующие Вас ниши')
        verbose_name_plural = _('Интересующие Вас ниши')


class UserInterestsThird(models.Model):
    interest = models.CharField(verbose_name=_('Интерес'), max_length=150)

    def __str__(self):
        return self.interest

    class Meta:
        verbose_name = _('Цели')
        verbose_name_plural = _('Цели')


class BeforeUniversity(models.Model):
    name = models.CharField(max_length=125, verbose_name=_('Наименования'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Образование')
        verbose_name_plural = _('Образование')


class University(models.Model):
    name = models.CharField(max_length=125, verbose_name=_('Наименования'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('ВУЗ')
        verbose_name_plural = _('ВУЗ')


class Course(models.Model):
    name = models.CharField(max_length=125, verbose_name=_('Наименования'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Курс')
        verbose_name_plural = _('Курс')


MANAGER_STATUSES = [
    (_('Manager Lead'), _('Лид менеджера')),
    (_('In Progress with Manager'), _('В работе у менеджера')),
    (_('Rejected'), _('Отказ')),
    (_('Awaiting Payment'), _('Ожидает оплаты')),
    (_('Partially Paid'), _('Частично оплачен')),
    (_('Paid'), _('Оплачен')),
]

EDUCATION_STATUSES = [
    (_('Base'), _('Базовый')),
    (_('Optimal'), _('Оптимальный')),
    (_('Advanced'), _('Продвинутый')),
    (_('Free participation'), _('Басплатное участие')),
    (_('Dropout'), _('Выбыл')),
    (_('Grant'), _('Грант')),
]


class Student(models.Model):
    # Обязательные поля
    full_name = models.CharField(max_length=255, verbose_name=_('ФИО'))
    mobile_phone = models.CharField(max_length=25, verbose_name=_('Мобильный телефон'))
    email = models.EmailField(verbose_name=_('Электронная почта'))
    tg_nickname = models.CharField(max_length=50, verbose_name=_('Ник в Телеграм'), unique=True)
    age = models.PositiveIntegerField(verbose_name=_('Возраст'))
    gender = models.CharField(max_length=50, verbose_name=_('Пол'))
    before_university = models.ForeignKey(BeforeUniversity, verbose_name=_('Образование'), on_delete=models.CASCADE)
    university = models.ForeignKey(University, verbose_name=_('ВУЗ'), on_delete=models.CASCADE)
    faculty = models.CharField(max_length=255, verbose_name=_('Факультет'))
    course = models.ForeignKey(Course, verbose_name=_('Курс'), on_delete=models.CASCADE)
    interest_first = models.ManyToManyField('UserInterestsFirst', verbose_name=_('Профессиональная сфера интересов'),
                                            blank=True)
    other_interest_first = models.CharField(max_length=150, verbose_name=_('Профессиональная сфера интересов другое'),
                                            null=True, blank=True)
    interest_second = models.ManyToManyField('UserInterestsSecond', verbose_name=_('Интересующие Вас ниши'),
                                             blank=True)
    other_interest_second = models.CharField(max_length=150, verbose_name=_('Интересующие Вас ниши другое'), null=True,
                                             blank=True)
    interest_third = models.ManyToManyField('UserInterestsThird', verbose_name=_('Цели'), blank=True)
    other_interest_third = models.CharField(max_length=150, verbose_name=_('цели другие'), null=True, blank=True)
    manager_status = models.CharField(max_length=50, choices=MANAGER_STATUSES, verbose_name=_('Статус менеджера'))
    education_status = models.CharField(max_length=50, choices=EDUCATION_STATUSES, verbose_name=_('Статус обучения'))

    hours_per_week = models.PositiveIntegerField(verbose_name=_('Сколько часов готовы уделять в неделю'))
    telegram_user_id = models.IntegerField(unique=True, null=True, blank=True, verbose_name='Телеграм ID User')
    projects = models.ManyToManyField('Project', related_name='students', blank=True, verbose_name=_('Проекты'))
    # total_rating = models.FloatField(max_length=255, default=0, verbose_name=_('Общий рейтинг'))
    subscription_end_date = models.DateField(verbose_name='Дата окончания подиски', blank=True, null=True)


    def __str__(self):
        return self.full_name

    def get_last_mailing(self):
        last_mailing = self.mailings.aggregate(last_sent=Max('sent_date'))['last_sent']
        if last_mailing:
            return self.mailings.get(sent_date=last_mailing)
        return None

    def projects_in_group(self):
        project_count = Project.objects.filter(group__students=self).annotate(num_projects=Count('id')).aggregate(
            total=Sum('num_projects'))['total']
        return project_count

    def calculate_total_rating(self):
        total_rating = self.student.aggregate(Sum('task_rating'))['task_rating__sum'] or 0
        return total_rating

    class Meta:
        verbose_name = _('Студент')
        verbose_name_plural = _('Студенты')


class StudentCV(models.Model):
    student = models.ForeignKey(Student, verbose_name=_('Студент'), on_delete=models.CASCADE)
    file = models.FileField(verbose_name=_('Резюме студента'), upload_to='student_cv')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))

    def __str__(self):
        if self.student:
            return self.student.full_name
        else:
            return "StudentCV without associated student"

    class Meta:
        verbose_name = _('Резюме студента')
        verbose_name_plural = _('Резюме студента')


class StudentPortfolio(models.Model):
    student = models.ForeignKey(Student, verbose_name=_('Студент'), on_delete=models.CASCADE)
    file = models.FileField(verbose_name=_('Портфолио студента'), upload_to='student_cv')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))

    def __str__(self):
        if self.student:
            return self.student.full_name
        else:
            return "StudentCV without associated student"

    class Meta:
        verbose_name = _('Портфолио студента')

        verbose_name_plural = _('Портфолио студента')


class GroupStudent(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название группы'))
    captain = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='captain_group_students')
    students = models.ManyToManyField(Student, related_name='group_students')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(GroupStudent, self).save(*args, **kwargs)
        group_projects = self.project_set.all()
        for student in self.students.all():
            student.projects.add(*group_projects)

    class Meta:
        verbose_name = _('Группа')
        verbose_name_plural = _('Группы')


class Project(models.Model):
    group = models.ManyToManyField(GroupStudent, verbose_name=_('Группа'))
    name = models.CharField(max_length=300, verbose_name=_('Наименование'))
    intricacy = models.CharField(max_length=250, verbose_name=_('Сложность'))
    start_date = models.DateField(verbose_name=_('Дата начала'), null=True, blank=True)
    end_date = models.DateField(verbose_name=_('Дата окончания'), null=True, blank=True)
    group_grade = models.FloatField(max_length=10, verbose_name=_('Групповая оценка'), blank=True, null=True)
    intricacy_coefficient = models.FloatField(max_length=10, verbose_name='Коэффициент сложности',
                                              blank=True, null=True,
                                              validators=[MinValueValidator(0), MaxValueValidator(1.5)])

    def __str__(self):
        return self.name

    @property
    def duration(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None

    def calculate_task_rating(self):
        if (
                self.task.all().filter(personal_grade__isnull=False).exists() and
                self.task.filter(deadline_compliance__isnull=False).exists() and
                self.task.filter(manager_recommendation__isnull=False).exists() and
                self.group_grade is not None and
                self.intricacy_coefficient is not None
        ):
            personal_grade_avg = self.task.filter(personal_grade__isnull=False).aggregate(Avg('personal_grade'))[
                'personal_grade__avg']
            deadline_compliance_avg = \
            self.task.filter(deadline_compliance__isnull=False).aggregate(Avg('deadline_compliance'))[
                'deadline_compliance__avg']
            manager_recommendation_avg = \
            self.task.filter(manager_recommendation__isnull=False).aggregate(Avg('manager_recommendation'))[
                'manager_recommendation__avg']

            rating = round(
                (
                        0.3 * personal_grade_avg +
                        0.2 * deadline_compliance_avg +
                        0.2 * manager_recommendation_avg +
                        0.3 * self.group_grade
                ) * self.intricacy_coefficient, 1
            )
            return rating

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        task_rating = self.calculate_task_rating()
        for task in self.task.all():
            task.task_rating = task_rating
            task.save()

    class Meta:
        verbose_name = _('Проект')
        verbose_name_plural = _('Проект')


class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Проект'))
    user = models.ForeignKey(User, verbose_name=_('админ'), on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Student, verbose_name=_('Капитан группы'), on_delete=models.CASCADE, null=True,
                                blank=True)
    comment_text = models.TextField(verbose_name=_('Текст комментария'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))

    def __str__(self):
        return self.project

    class Meta:
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')


class TestTask(models.Model):
    description = models.TextField(verbose_name=_('Описание'))
    project_cost = models.CharField(max_length=120, verbose_name=_("Стоимость"), null=True, blank=True)
    start_date = models.DateField(verbose_name=_('Дата начала'), null=True, blank=True)
    end_date = models.DateField(verbose_name=_('Дата окончания'), null=True, blank=True)
    grade = models.IntegerField(verbose_name=_('оценка'), null=True, blank=True)

    def __str__(self):
        return self.description

    @property
    def execution_period(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None

    class Meta:
        verbose_name = _('Задача тесовое')
        verbose_name_plural = _('Задача тестовое')


class AnswerTestTask(models.Model):
    file = models.FileField(verbose_name=_('Ответ файлом'), upload_to='file_a', null=True, blank=True)
    url = models.URLField(verbose_name=_('Ответ ссылкой'), null=True, blank=True)
    answer = models.ForeignKey(TestTask, verbose_name=_('Ответ по задаче'), on_delete=models.CASCADE, null=True,
                               blank=True)
    user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name = _('Ответы')
        verbose_name_plural = _('Ответы')


class TaskGroup(models.Model):
    project = models.ForeignKey(Project, verbose_name=_('Проект'), on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(verbose_name=_('Описание'))
    project_cost = models.CharField(max_length=120, verbose_name=_("Стоимость"), null=True, blank=True)
    start_date = models.DateField(verbose_name=_('Дата начала'), null=True, blank=True)
    end_date = models.DateField(verbose_name=_('Дата окончания'), null=True, blank=True)
    grade = models.IntegerField(verbose_name=_('оценка'), null=True, blank=True)

    def __str__(self):
        return self.description

    @property
    def execution_period(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None

    class Meta:
        verbose_name = _('Задача группы по проекту')
        verbose_name_plural = _('Задача группы по проекту')


STATUS_CHOICES = [
    ('in_progress', _('В работу')),
    ('being_performed', _('Выполняется')),
    ('completed', _('Выполнена')),
    ('awaiting_os', _('Ожидает ОС')),
    ('under_revision', _('На правках')),
    ('finished', _('Завершена')),
    ('on_pause', _('На паузе')),
]


class AnswerGroup(models.Model):
    file = models.FileField(verbose_name=_('Ответ файлом'), upload_to='file_a', null=True, blank=True)
    url = models.URLField(verbose_name=_('Ответ ссылкой'), null=True, blank=True)
    answer = models.ForeignKey(TaskGroup, verbose_name=_('Ответ группы'), on_delete=models.CASCADE, null=True,
                               blank=True)
    user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name = _('Ответ группы')
        verbose_name_plural = _('Ответ группы')


class TaskStatusGroup(models.Model):
    task_group = models.ForeignKey(TaskGroup, verbose_name=_('Задача группы'), on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    status = models.CharField(max_length=50, verbose_name=_('Статус'), choices=STATUS_CHOICES)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = _('Статус задачи группы')
        verbose_name_plural = _('Статус задачи группы')


class TaskStudent(models.Model):
    project = models.ForeignKey(Project, verbose_name=_('Проект'), on_delete=models.CASCADE, null=True, blank=True,
                                related_name='task')
    student = models.ForeignKey(Student, verbose_name=_('Студент'), on_delete=models.CASCADE, related_name='student')
    description = models.TextField(verbose_name=_('Описание'))
    project_cost = models.CharField(max_length=120, verbose_name=_("Стоимость"), null=True, blank=True)
    start_date = models.DateField(verbose_name=_('Дата начала'), null=True, blank=True)
    end_date = models.DateField(verbose_name=_('Дата окончания'), null=True, blank=True)
    personal_grade = models.FloatField(max_length=10, verbose_name=_('Личная оценка'), blank=True, null=True)
    deadline_compliance = models.FloatField(max_length=10, verbose_name=_('Соблюдение дедлайнов'), blank=True,
                                            null=True)
    manager_recommendation = models.FloatField(max_length=10, verbose_name=_('Рекомендация менеджера'), blank=True,
                                               null=True)
    task_rating = models.FloatField(max_length=255, verbose_name='Рейтинг за задачу', blank=True, null=True)

    def __str__(self):
        if self.student:
            return self.student.full_name
        else:
            return "No student assigned"

    @property
    def execution_period(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None

    def calculate_task_rating(self):
        if self.personal_grade is not None and self.deadline_compliance is not None and \
                self.manager_recommendation is not None and self.project.group_grade is not None and \
                self.project.intricacy_coefficient is not None:
            rating = round((0.3 * self.personal_grade + 0.2 * self.deadline_compliance +
                            0.2 * self.manager_recommendation + 0.3 * self.project.group_grade)
                           * self.project.intricacy_coefficient, 1)
            return rating

    def save(self, *args, **kwargs):
        task_rating = self.calculate_task_rating()
        self.task_rating = task_rating
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Задача студента по проекту')
        verbose_name_plural = _('Задача студента по проекту')


class AnswersStudent(models.Model):
    file = models.FileField(verbose_name='Ответ файлом', upload_to='file_a', null=True, blank=True)
    url = models.URLField(verbose_name='Ответ ссылкой', null=True, blank=True)
    answer = models.ForeignKey(TaskStudent, verbose_name='Ответ на задачу', on_delete=models.CASCADE, null=True,
                               blank=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name = _('Ответ студента')
        verbose_name_plural = _('Ответ студента')


class TaskStatusStudent(models.Model):
    task_student = models.ForeignKey(TaskStudent, verbose_name=_('Задача студента'), on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    status = models.CharField(max_length=50, verbose_name=_('Статус'), choices=STATUS_CHOICES)

    def __str__(self):
        return self.task_student

    class Meta:
        verbose_name = _('Статус задачи студента')
        verbose_name_plural = _('Статус задачи студента')


class File(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Имя файла'), blank=True, null=True)
    file = models.FileField(upload_to='Files', verbose_name=_('Файлы'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Файл')
        verbose_name_plural = _('Файлы')


class DataKnowledgeFree(models.Model):
    chapter = models.ForeignKey('Chapter', verbose_name=_('Раздел'), on_delete=models.CASCADE)
    under_section = models.ForeignKey('UnderSection', verbose_name=_('Под раздел'), on_delete=models.CASCADE)
    title = models.TextField(verbose_name=_('Тема'))
    url = models.TextField(verbose_name=_('Ссылки'))
    files = models.ManyToManyField('File', verbose_name='Файлы')

    def __str__(self):
        return self.chapter.name

    class Meta:
        verbose_name = _('База знаний бесплатно')
        verbose_name_plural = _('База знаний бесплатно')


class Chapter(models.Model):
    name = models.CharField(verbose_name=_('Раздел'), max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Разделы')
        verbose_name_plural = _('Разделы')


class UnderSection(models.Model):
    name = models.CharField(verbose_name=_('Под раздел'), max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Раздел Образование')
        verbose_name_plural = _('Раздел Образование')


class DataKnowledge(models.Model):
    chapter = models.ForeignKey(Chapter, verbose_name=_('Раздел'), on_delete=models.CASCADE)
    under_section = models.ForeignKey(UnderSection, verbose_name=_('Под раздел'), on_delete=models.CASCADE)
    title = models.TextField(verbose_name=_('Тема'))
    url = models.TextField(verbose_name=_('Ссылки'))
    files = models.ManyToManyField('File', verbose_name='Файлы')

    def __str__(self):
        return self.chapter.name

    class Meta:
        verbose_name = _('База знаний платно')
        verbose_name_plural = _('База знаний платно')


class Mailing(models.Model):
    subject = models.CharField(max_length=225, verbose_name=_('Тема'))
    title = models.CharField(max_length=255, verbose_name=_('Заголовок'))
    message = models.TextField(verbose_name=_('Сообщение'))
    photo = models.ImageField(verbose_name=_('Фото'), null=True, blank=True, upload_to='img_mailing')
    sent_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата отправки'))
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='mailings', verbose_name=_('Студент'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Рассылка')
        verbose_name_plural = _('Рассылки')


class Orders(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name=_('дата создания'))
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='orders', verbose_name=_('Студент'))
    description = models.TextField(verbose_name=_('Описание'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Сумма'))
    payment_status = models.BooleanField(default=False, verbose_name=_('Статус оплаты'))

    def __str__(self):
        return str(self.student)

    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')


