from rest_framework import serializers
from .models import Administrator, Announcements, Courses


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = "__all__"

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcements
        fields = "__all__"