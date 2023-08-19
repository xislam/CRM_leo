from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveUpdateAPIView, ListAPIView
from .models import Student  # Предположим, у вас есть модель Student
from .serializers import StudentSerializer  # Предположим, у вас есть сериализатор StudentSerializer


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
