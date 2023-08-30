from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models import Max
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


class User(AbstractUser):
    full_name = models.CharField(max_length=255, verbose_name='ФИО', blank=True, null=True)
    mobile_phone = models.CharField(max_length=15, verbose_name='Мобильный телефон', blank=True, null=True)
    email = models.EmailField(verbose_name='Электронная почта', blank=True, null=True)
    tg_nickname = models.CharField(max_length=50, verbose_name='Ник в Телеграм', blank=True, null=True)
    age = models.PositiveIntegerField(verbose_name='Возраст', blank=True, null=True)
    gender = models.CharField(max_length=10, verbose_name='Пол', blank=True, null=True)
    university = models.CharField(max_length=255, verbose_name='ВУЗ', blank=True, null=True)
    course = models.PositiveIntegerField(verbose_name='Курс', blank=True, null=True)
    faculty = models.CharField(max_length=255, verbose_name='Факультет', blank=True, null=True)

    STATUS_CHOICES = (
        ('previous_flow', 'Прошлый поток'),
        ('subscribed_to_chatbot', 'Подписан на чат-бот'),
        ('lead', 'Лид'),
        ('in_progress', 'В работе у менеджера'),
        ('rejected', 'Отказ'),
        ('awaiting_payment', 'Ожидает оплаты'),
        ('partially_paid', 'Частично оплачен'),
        ('paid', 'Оплачен'),
        ('graduate', 'Выпускник'),
        ('working_group', 'Рабочая группа'),
        ('dropout', 'Выбыл'),
    )
    status = models.CharField(max_length=30, verbose_name='Статус', choices=STATUS_CHOICES, blank=True, null=True)
    # objects = CustomUserManager()


class UserInterestsFirst(models.Model):
    interest = models.CharField(verbose_name='Интерес', max_length=150)

    def __str__(self):
        return self.interest

    class Meta:
        verbose_name = 'Профессиональная сфера интересов'
        verbose_name_plural = 'Профессиональная сфера интересов'


class UserInterestsSecond(models.Model):
    interest = models.CharField(verbose_name='Интерес', max_length=150)

    def __str__(self):
        return self.interest

    class Meta:
        verbose_name = 'Интересующие Вас ниши'
        verbose_name_plural = 'Интересующие Вас ниши'


class UserInterestsThird(models.Model):
    interest = models.CharField(verbose_name='Интерес', max_length=150)

    def __str__(self):
        return self.interest

    class Meta:
        verbose_name = 'Цели'
        verbose_name_plural = 'Цели'


class BeforeUniversity(models.Model):
    name = models.CharField(max_length=125, verbose_name='Наименования')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Образование'
        verbose_name_plural = 'Образование'


class University(models.Model):
    name = models.CharField(max_length=125, verbose_name='Наименования')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ВУЗ'
        verbose_name_plural = 'ВУЗ'


class Course(models.Model):
    name = models.CharField(max_length=125, verbose_name='Наименования')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курс'


MANAGER_STATUSES = [
    ('lead', 'Лид'),
    ('in_progress', 'В работе у менеджера'),
    ('rejected', 'Отказ'),
    ('waiting_for_payment', 'Ожидает оплаты'),
    ('partially_paid', 'Частично оплачен'),
    ('paid', 'Оплачен'),
]

EDUCATION_STATUSES = [
    ('free_subscription_registration', 'Регистрация на бесплатную подписку'),
    ('completed_free_subscription', 'Завершена бесплатная подписка'),
    ('paid_subscription_member', 'Участник платной подписки'),
    ('course_participant', 'Участник курса'),
    ('dropped_out', 'Выбыл'),
    ('completed_education', 'Завершил обучение'),
]


class Student(models.Model):
    # Обязательные поля
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    mobile_phone = models.CharField(max_length=15, verbose_name='Мобильный телефон')
    email = models.EmailField(verbose_name='Электронная почта')
    tg_nickname = models.CharField(max_length=50, verbose_name='Ник в Телеграм', unique=True)
    age = models.PositiveIntegerField(verbose_name='Возраст')
    gender = models.CharField(max_length=10, verbose_name='Пол')
    before_university = models.ForeignKey(BeforeUniversity, verbose_name='Образование', on_delete=models.CASCADE)
    university = models.ForeignKey(University, verbose_name='ВУЗ', on_delete=models.CASCADE)
    faculty = models.CharField(max_length=255, verbose_name='Факультет')
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE)
    interest_first = models.ManyToManyField('UserInterestsFirst', verbose_name='Профессиональная сфера интересов',
                                            blank=True)
    other_interest_first = models.CharField(max_length=150, verbose_name='Профессиональная сфера интересов другое',
                                            null=True, blank=True)
    interest_second = models.ManyToManyField('UserInterestsSecond', verbose_name='Интересующие Вас ниши',
                                             blank=True)
    other_interest_second = models.CharField(max_length=150, verbose_name='Интересующие Вас ниши другое', null=True,
                                             blank=True)
    interest_third = models.ManyToManyField('UserInterestsThird', verbose_name='Цели', blank=True)
    other_interest_third = models.CharField(max_length=150, verbose_name='цели другие', null=True, blank=True)
    manager_status = models.CharField(max_length=20, choices=MANAGER_STATUSES, verbose_name='Статус менеджера')
    education_status = models.CharField(max_length=30, choices=EDUCATION_STATUSES, verbose_name='Статус обучения')

    # Дополнительное поле
    hours_per_week = models.PositiveIntegerField(verbose_name='Сколько часов готовы уделять в неделю')

    def __str__(self):
        return self.full_name

    def get_last_mailing(self):
        last_mailing = self.mailings.aggregate(last_sent=Max('sent_date'))['last_sent']
        if last_mailing:
            return self.mailings.get(sent_date=last_mailing)
        return None

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class StudentCV(models.Model):
    student = models.ForeignKey(Student, verbose_name='Студент', on_delete=models.CASCADE)
    file = models.FileField(verbose_name='Резюме студента', upload_to='student_cv')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.student.full_name

    class Meta:
        verbose_name = 'Резюме студента'
        verbose_name_plural = 'Резюме студента'


class StudentPortfolio(models.Model):
    student = models.ForeignKey(Student, verbose_name='Студент', on_delete=models.CASCADE)
    file = models.FileField(verbose_name='Портфолио студента', upload_to='student_cv')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.student.full_name

    class Meta:
        verbose_name = 'Портфолио студента'
        verbose_name_plural = 'Портфолио студента'


class GroupStudent(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название группы')
    captain = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='captain_group_students')
    students = models.ManyToManyField(Student, related_name='group_students')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Project(models.Model):
    group = models.ManyToManyField(GroupStudent, verbose_name='Группа')
    name = models.CharField(max_length=300, verbose_name='Наименование')
    intricacy = models.CharField(max_length=250, verbose_name='Сложность')
    duration = models.CharField(max_length=250, verbose_name='Длительность')
    start_date = models.DateField(verbose_name='Дата начала', null=True, blank=True)
    end_date = models.DateField(verbose_name='Дата окончания', null=True, blank=True)
    grade = models.CharField(max_length=250, verbose_name='Оценка')

    def __str__(self):
        return self.name

    @property
    def duration(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проект'


class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments', verbose_name='Проект')
    user = models.ForeignKey(User, verbose_name='админ', on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Student, verbose_name='Капитан группы', on_delete=models.CASCADE, null=True, blank=True)
    comment_text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Проект: {self.project} Студент: {self.student.full_name} Админ: {self.user.full_name}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class TestTask(models.Model):
    description = models.TextField(verbose_name='Описание')
    project_cost = models.CharField(max_length=120, verbose_name="Стоимость", null=True, blank=True)
    start_date = models.DateField(verbose_name='Дата начала', null=True, blank=True)
    end_date = models.DateField(verbose_name='Дата окончания', null=True, blank=True)
    grade = models.IntegerField(verbose_name='оценка', null=True, blank=True)

    def __str__(self):
        return self.description

    @property
    def execution_period(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None

    class Meta:
        verbose_name = 'Задача тесовое'
        verbose_name_plural = 'Задача тестовое'


class AnswerTestTask(models.Model):
    file = models.FileField(verbose_name='Ответ файлом', upload_to='file_a', null=True, blank=True)
    url = models.URLField(verbose_name='Ответ ссылкой', null=True, blank=True)
    answer = models.ForeignKey(TestTask, verbose_name='Ответ по задаче', on_delete=models.CASCADE, null=True,
                               blank=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name = 'Ответы'
        verbose_name_plural = 'Ответы'


class TaskGroup(models.Model):
    project = models.ForeignKey(Project, verbose_name='Проект', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(verbose_name='Описание')
    project_cost = models.CharField(max_length=120, verbose_name="Стоимость", null=True, blank=True)
    start_date = models.DateField(verbose_name='Дата начала', null=True, blank=True)
    end_date = models.DateField(verbose_name='Дата окончания', null=True, blank=True)
    grade = models.IntegerField(verbose_name='оценка', null=True, blank=True)

    def __str__(self):
        return self.description

    @property
    def execution_period(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None

    class Meta:
        verbose_name = 'Задача группы по проекту'
        verbose_name_plural = 'Задача группы по проекту'


STATUS_CHOICES = [
    ('В работу', 'В работу'),
    ('Выполняется', 'Выполняется'),
    ('Выполнена', 'Выполнена'),
    ('Ожидает ОС', 'Ожидает ОС'),
    ('На правках', 'На правках'),
    ('Завершена', 'Завершена'),
    ('На паузе', 'На паузе'),
]


class AnswerGroup(models.Model):
    file = models.FileField(verbose_name='Ответ файлом', upload_to='file_a', null=True, blank=True)
    url = models.URLField(verbose_name='Ответ ссылкой', null=True, blank=True)
    answer = models.ForeignKey(TaskGroup, verbose_name='Ответ группы', on_delete=models.CASCADE, null=True,
                               blank=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name = 'Ответ группы'
        verbose_name_plural = 'Ответ группы'


class TaskStatusGroup(models.Model):
    task_group = models.ForeignKey(TaskGroup, verbose_name='Задача группы', on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=50, verbose_name='Статус', choices=STATUS_CHOICES)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Статус задачи группы'
        verbose_name_plural = 'Статус задачи группы'


class TaskStudent(models.Model):
    project = models.ForeignKey(Project, verbose_name='Проект', on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Student, verbose_name='Студент', on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Описание')
    project_cost = models.CharField(max_length=120, verbose_name="Стоимость", null=True, blank=True)
    start_date = models.DateField(verbose_name='Дата начала', null=True, blank=True)
    end_date = models.DateField(verbose_name='Дата окончания', null=True, blank=True)
    grade = models.IntegerField(verbose_name='оценка', null=True, blank=True)

    def __str__(self):
        return self.student.full_name

    @property
    def execution_period(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None

    class Meta:
        verbose_name = 'Задача студента по проекту'
        verbose_name_plural = 'Задача студента по проекту'


class AnswersStudent(models.Model):
    file = models.FileField(verbose_name='Ответ файлом', upload_to='file_a', null=True, blank=True)
    url = models.URLField(verbose_name='Ответ ссылкой', null=True, blank=True)
    answer = models.ForeignKey(TaskStudent, verbose_name='Ответ на задачу', on_delete=models.CASCADE, null=True,
                               blank=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name = 'Ответ студента'
        verbose_name_plural = 'Ответ студента'


class TaskStatusStudent(models.Model):
    task_student = models.ForeignKey(TaskStudent, verbose_name='Задача студента', on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=50, verbose_name='Статус', choices=STATUS_CHOICES)

    def __str__(self):
        return self.task_student

    class Meta:
        verbose_name = 'Статус задачи студента'
        verbose_name_plural = 'Статус задачи студента'





class DataKnowledgeFree(models.Model):
    chapter = models.ForeignKey('Chapter', verbose_name='Раздел', on_delete=models.CASCADE)
    under_section = models.ForeignKey('UnderSection', verbose_name='Под раздел', on_delete=models.CASCADE)
    title = models.TextField(verbose_name='Тема')
    url = models.TextField(verbose_name='Ссылки')

    def __str__(self):
        return self.chapter.name

    class Meta:
        verbose_name = 'База знаний бесплатно'
        verbose_name_plural = 'База знаний бесплатно'


class Chapter(models.Model):
    name = models.CharField(verbose_name='Раздел', max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Разделы'
        verbose_name_plural = 'Разделы'


class UnderSection(models.Model):
    name = models.CharField(verbose_name='Под раздел', max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Раздел Образование'
        verbose_name_plural = 'Раздел Образование'


class DataKnowledge(models.Model):
    chapter = models.ForeignKey(Chapter, verbose_name='Раздел', on_delete=models.CASCADE)
    under_section = models.ForeignKey(UnderSection, verbose_name='Под раздел', on_delete=models.CASCADE)
    title = models.TextField(verbose_name='Тема')
    url = models.TextField(verbose_name='Ссылки')

    def __str__(self):
        return self.chapter.name

    class Meta:
        verbose_name = 'База знаний платно'
        verbose_name_plural = 'База знаний платно'


class Mailing(models.Model):
    subject = models.CharField(max_length=225, verbose_name='Тема')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    message = models.TextField(verbose_name='Сообщение')
    photo = models.ImageField(verbose_name='Фото', null=True, blank=True, upload_to='img_mailing')
    sent_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='mailings')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
