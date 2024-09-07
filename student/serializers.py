from quiz.models import Questions
from rest_framework import serializers
from .models import QuizScore, Student, SubjectSelection, SubmitedAssignment


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

class SubjectSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectSelection
        fields = "__all__"

class SubmitedAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmitedAssignment
        fields = ["assignment","student","assignment_solution","course"]

class ViewGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmitedAssignment
        fields = "__all__"

class QuizTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ["question_id","question","quiz_id","question_type","options","marks"]

class QuizTotalMarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizScore
        fields = ['marks_scored',"student","quiz"]