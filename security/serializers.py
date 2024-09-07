from rest_framework import serializers
from security.models import AdminAuthTokens, ProfessorAuthTokens, StudentAuthTokens

class AdminAuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAuthTokens
        fields = "__all__"

class ProfessorAuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessorAuthTokens
        fields = "__all__"

class StudentAuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAuthTokens
        fields = "__all__"