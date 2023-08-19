from django.urls import path
from .views import StudentCreateView, StudentDetailUpdateView, StudentListView

urlpatterns = [
    path('create/', StudentCreateView.as_view(), name='student-create'),
    path('detail-update/<str:tg_nickname>/', StudentDetailUpdateView.as_view(), name='student-detail-update'),
    path('list/', StudentListView.as_view(), name='student-list'),

]
