from rest_framework import serializers
from student.models import SubmitedAssignment
from .models import Assignment, Notes, ProfsAnnouncements

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = "__all__"

class ProfsAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfsAnnouncements
        fields = "__all__"

class CheckAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmitedAssignment
        fields = ["assigned_marks"]
