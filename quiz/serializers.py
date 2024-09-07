from rest_framework import serializers
from .models import Questions, Quiz

class   QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = "__all__"

class UpdateQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['question','question_type','answer','options','marks']

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__" 

