from django.urls import path

from . import views
from .views import StudentCreateView, StudentDetailUpdateView, StudentListView, StudentListMailingView, CourseListView, \
    StudentCvCreateView

urlpatterns = [
    path('create/', StudentCreateView.as_view(), name='student-create'),
    path('detail-update/<str:tg_nickname>/', StudentDetailUpdateView.as_view(), name='student-detail-update'),
    path('list/', StudentListView.as_view(), name='student-list'),
    path('students/', StudentListMailingView.as_view(), name='student-list-mailing'),
    path('user_interests_first/', views.UserInterestsFirstList.as_view(), name='user_interests_first-list'),
    path('user_interests_second/', views.UserInterestsSecondList.as_view(), name='user_interests_second-list'),
    path('user_interests_third/', views.UserInterestsThirdFirstList.as_view(), name='user_interests_third-list'),
    path('user_before_university/', views.BeforeUniversityFirstList.as_view(), name='user_interests_university-list'),
    path('user_university/', views.UniversityListView.as_view(), name='user_university-list'),
    path('student_cv/<str:student__telegram_user_id>/', views.StudentCVDetailView.as_view(), name='studentcv-detail'),
    path('groups/', views.GroupStudentListView.as_view(), name='groupstudent-list'),
    path('groups/<int:pk>/', views.GroupStudentDetailView.as_view(), name='groupstudent-detail'),
    path('projects/', views.ProjectListView.as_view(), name='project-list'),
    path('comments/', views.CommentListView.as_view(), name='comment-list'),
    path('answertesttasks/', views.AnswerTestTaskListView.as_view(), name='answertesttask-list'),
    path('taskgroups/', views.TaskGroupListView.as_view(), name='taskgroup-list'),
    path('answergroups/', views.AnswerGroupListView.as_view(), name='answergroup-list'),
    path('answergroups/create/', views.AnswerGroupListView.as_view(), name='answergroup-create'),
    path('taskstatusgroups/', views.TaskStatusGroupListView.as_view(), name='taskstatusgroup-list'),
    path('answersstudents/', views.AnswersStudentListView.as_view(), name='answersstudent-list'),
    path('answersstudents/create/', views.AnswersStudentListView.as_view(), name='answersstudent-create'),
    path('taskstatusstudents/', views.TaskStatusStudentListView.as_view(), name='taskstatusstudent-list'),
    path('dataknowledgefree/', views.DataKnowledgeFreeListView.as_view(), name='dataknowledgefree-list'),
    path('dataknowledge/', views.DataKnowledgeListView.as_view(), name='dataknowledge-list'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('dataknowledge/<str:chapter>/', views.DataKnowledgeByChapter.as_view(), name='dataknowledge-by-chapter'),
    path('dataknowledgefree/<str:chapter>/', views.DataKnowledgeFreeByChapter.as_view(),
         name='dataknowledgefree-by-chapter'),
    path('create-student-cv/<int:telegram_user_id>', StudentCvCreateView.as_view(), name='create-student-cv'),
    ##### Добавления
    path('robokassa-result/', views.robokassa_result, name='robokassa_result'),

]
