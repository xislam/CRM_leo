import django_filters
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, FormView
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveUpdateAPIView, ListAPIView
from django_filters import rest_framework as filters
from rest_framework.response import Response

from .filters import StudentFilter
from .forms import StudentFilterForm, MailingForm
from .models import Student, Mailing, UserInterestsFirst, UserInterestsSecond, \
    UserInterestsThird, BeforeUniversity, StudentCV, GroupStudent, Project, \
    Comment, User, AnswerTestTask, TaskGroup, AnswerGroup, TaskStatusGroup, \
    TaskStudent, AnswersStudent, TaskStatusStudent, DataKnowledgeFree, \
    DataKnowledge, University, Course  # Предположим, у вас есть модель Student
from .serializers import StudentSerializer, \
    UserInterestsFirstSerializer, \
    UserInterestsSecondSerializer, \
    UserInterestsThirdSerializer, BeforeUniversitySerializer, \
    StudentCVSerializer, GroupStudentSerializer, \
    ProjectSerializer, CommentSerializer, \
    AnswerTestTaskSerializer, TaskGroupSerializer, \
    AnswerGroupSerializer, TaskStatusGroupSerializer, \
    TaskStudentSerializer, AnswersStudentSerializer, \
    TaskStatusStudentSerializer, DataKnowledgeFreeSerializer, \
    DataKnowledgeSerializer, UniversitySerializer, \
    CourseSerializer  # Предположим, у вас есть сериализатор StudentSerializer


class StudentCreateView(CreateAPIView):
    queryset = Student.objects.all()  # Здесь вы можете указать желаемый queryset
    serializer_class = StudentSerializer


class StudentDetailUpdateView(RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'tg_nickname'


class StudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StudentFilter


class StudentListMailingView(ListView):
    model = Student
    template_name = 'student_list_mailing.html'
    context_object_name = 'students'
    paginate_by = 10  # Количество студентов на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        form = StudentFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['university']:
                queryset = queryset.filter(university=form.cleaned_data['university'])
            if form.cleaned_data['course']:
                queryset = queryset.filter(course=form.cleaned_data['course'])
            if form.cleaned_data['before_university']:
                queryset = queryset.filter(before_university=form.cleaned_data['before_university'])
            if form.cleaned_data['manager_status']:
                queryset = queryset.filter(manager_status=form.cleaned_data['manager_status'])
            if form.cleaned_data['education_status']:
                queryset = queryset.filter(education_status=form.cleaned_data['education_status'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = StudentFilterForm(self.request.GET)

        # Если есть POST-данные рассылки, создайте форму с этими данными
        mailing_form = MailingForm(self.request.POST)
        context['mailing_form'] = mailing_form

        return context

    def post(self, request, *args, **kwargs):
        mailing_form = MailingForm(request.POST, request.FILES)
        if mailing_form.is_valid():
            selected_students_ids = request.POST.getlist('selected_students')
            selected_students = Student.objects.filter(id__in=selected_students_ids)

            if selected_students:
                for student in selected_students:
                    # Создаем рассылку для каждого студента
                    mailing = mailing_form.save(commit=False)
                    mailing.student = student
                    mailing.save()

                    # Выполните действия для отправки почты, включая прикрепление изображения
                    # Здесь вы можете использовать SMTP-сервер или другой метод отправки почты.
                    # Отправка рассылки и другие необходимые действия

                messages.success(request, "Рассылка успешно создана и отправлена.")
                return HttpResponseRedirect(reverse('student-list-mailing'))  # Замените 'success_url_name'

            else:
                messages.error(request, "Вы должны выбрать хотя бы одного студента перед созданием рассылки.")
                # Если есть ошибка, вернемся к отображению страницы с формой рассылки и ошибкой
                return self.get(request, *args, **kwargs)

        return render(request, self.template_name, {'mailing_form': mailing_form})


class UserInterestsFirstList(generics.ListAPIView):
    queryset = UserInterestsFirst.objects.all()
    serializer_class = UserInterestsFirstSerializer


class UserInterestsSecondList(generics.ListAPIView):
    queryset = UserInterestsSecond.objects.all()
    serializer_class = UserInterestsSecondSerializer


class UserInterestsThirdFirstList(generics.ListAPIView):
    queryset = UserInterestsThird.objects.all()
    serializer_class = UserInterestsThirdSerializer


class BeforeUniversityFirstList(generics.ListAPIView):
    queryset = BeforeUniversity.objects.all()
    serializer_class = BeforeUniversitySerializer


class StudentCVDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentCV.objects.all()
    serializer_class = StudentCVSerializer
    lookup_field = 'student__telegram_user_id'



class GroupStudentListView(generics.ListAPIView):
    queryset = GroupStudent.objects.all()
    serializer_class = GroupStudentSerializer


class GroupStudentDetailView(generics.RetrieveAPIView):
    queryset = GroupStudent.objects.all()
    serializer_class = GroupStudentSerializer


class ProjectFilter(filters.FilterSet):
    class Meta:
        model = Project
        fields = {
            'group__name': ['exact'],
            'name': ['icontains'],
        }


class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filterset_class = ProjectFilter


class CommentFilter(filters.FilterSet):
    class Meta:
        model = Comment
        fields = {
            'project__name': ['exact'],
        }


class CommentListView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filterset_class = CommentFilter

    def perform_create(self, serializer):
        tg_nickname = self.request.data.get('tg_nickname')
        if tg_nickname:
            user = User.objects.get(tg_nickname=tg_nickname)
            serializer.save(user=user)
        else:
            serializer.save()


class AnswerTestTaskListView(generics.ListCreateAPIView):
    queryset = AnswerTestTask.objects.all()
    serializer_class = AnswerTestTaskSerializer


class TaskGroupFilter(django_filters.FilterSet):
    class Meta:
        model = TaskGroup
        fields = {
            'project__name': ['exact'],
        }


class TaskGroupListView(generics.ListAPIView):
    queryset = TaskGroup.objects.all()
    serializer_class = TaskGroupSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = TaskGroupFilter


class AnswerGroupListView(generics.ListCreateAPIView):
    queryset = AnswerGroup.objects.all()
    serializer_class = AnswerGroupSerializer


class TaskStatusGroupListView(generics.ListCreateAPIView):
    queryset = TaskStatusGroup.objects.all()
    serializer_class = TaskStatusGroupSerializer


class TaskStudentFilter(filters.FilterSet):
    class Meta:
        model = TaskStudent
        fields = {
            'student__tg_nickname': ['exact'],
        }


class TaskStudentListView(generics.ListCreateAPIView):
    queryset = TaskStudent.objects.all()
    serializer_class = TaskStudentSerializer
    filterset_class = TaskStudentFilter


class AnswersStudentListView(generics.ListCreateAPIView):
    queryset = AnswersStudent.objects.all()
    serializer_class = AnswersStudentSerializer


class TaskStatusStudentListView(generics.ListCreateAPIView):
    queryset = TaskStatusStudent.objects.all()
    serializer_class = TaskStatusStudentSerializer


class DataKnowledgeFreeListView(generics.ListAPIView):
    queryset = DataKnowledgeFree.objects.all()
    serializer_class = DataKnowledgeFreeSerializer


class DataKnowledgeListView(generics.ListAPIView):
    queryset = DataKnowledge.objects.all()
    serializer_class = DataKnowledgeSerializer


class UniversityListView(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class StudentCvCreateView(generics.CreateAPIView):
    serializer_class = StudentCVSerializer

    def create(self, request, *args, **kwargs):
        telegram_user_id = self.kwargs.get('telegram_user_id')
        student = Student.objects.filter(telegram_user_id=telegram_user_id).first()
        if student:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(student=student)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Студент с указанным Telegram ID не найден.'}, status=status.HTTP_404_NOT_FOUND)
