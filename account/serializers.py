from rest_framework import serializers
from .models import Student, UserInterestsFirst, UserInterestsSecond, UserInterestsThird, BeforeUniversity, University, \
    Course, StudentCV, GroupStudent, Project, Comment, AnswerTestTask, TaskGroup, AnswerGroup, TaskStatusGroup, \
    TaskStudent, AnswersStudent, TaskStatusStudent, DataKnowledgeFree, Chapter, \
    UnderSection, DataKnowledge, File, Orders


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class UserInterestsFirstSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterestsFirst
        fields = '__all__'


class UserInterestsSecondSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterestsSecond
        fields = '__all__'


class UserInterestsThirdSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterestsThird
        fields = '__all__'


class BeforeUniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BeforeUniversity
        fields = '__all__'


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class StudentCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCV
        fields = '__all__'


class StudentPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCV
        fields = '__all__'


class GroupStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStudent
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class AnswerTestTaskSerializer(serializers.ModelSerializer):
    tg_nickname = serializers.CharField(source='user.tg_nickname', read_only=True)

    class Meta:
        model = AnswerTestTask
        fields = '__all__'


class TaskGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroup
        fields = '__all__'


class TaskStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStudent
        fields = '__all__'


class AnswerGroupSerializer(serializers.ModelSerializer):
    tg_nickname = serializers.CharField(source='user.tg_nickname', read_only=True)

    class Meta:
        model = AnswerGroup
        fields = '__all__'


class TaskStatusGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatusGroup
        fields = '__all__'


class TaskStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStudent
        fields = '__all__'


class AnswersStudentSerializer(serializers.ModelSerializer):
    tg_nickname = serializers.CharField(source='user.tg_nickname', read_only=True)

    class Meta:
        model = AnswersStudent
        fields = '__all__'


class TaskStatusStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatusStudent
        fields = '__all__'


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'


class UnderSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnderSection
        fields = '__all__'


class DataKnowledgeSerializer(serializers.ModelSerializer):
    chapter = ChapterSerializer()
    under_section = UnderSectionSerializer()

    class Meta:
        model = DataKnowledge
        fields = '__all__'


class DataKnowledgeFreeSerializer(serializers.ModelSerializer):
    chapter = ChapterSerializer()
    under_section = UnderSectionSerializer()

    class Meta:
        model = DataKnowledgeFree
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class DataKnowledgeFileSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = DataKnowledge
        fields = '__all__'


class DataKnowledgeFreeFileSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = DataKnowledgeFree
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'
