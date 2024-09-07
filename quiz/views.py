from common.constants import (
    ANS_MUST_BE_TRUE_OR_FALSE,
    BAD_REQUEST,
    OPTIONS_ARE_MISSING,
    QUESTION_CREATED_SUCCESSFULLY,
    QUESTION_DELETED_SUCCESSFULLY,
    QUESTION_FETCHED_SUCCESSFULLY,
    QUESTION_UPDATED_SUCCESSFULLY,
    QUIZ_CREATED_SUCCESSFULLY,
    QUIZ_DELETED_SUCCESSFULLY,
    QUIZ_FETCHED_SUCCESSFULLY,
    QUIZ_UPDATED_SUCCESSFULLY
)
from exceptions.generic import CustomBadRequest, GenericException
from exceptions.generic_response import GenericSuccessResponse
from .models import Questions, Quiz
from .serializers import QuestionsSerializer, QuizSerializer, UpdateQuestionsSerializer
from rest_framework.views import APIView
from security.professor_authorization import ProfessorJWTAuthentication


class ManageQuiz(APIView):
    authentication_classes = [ProfessorJWTAuthentication]

    @staticmethod
    def get(request):
        try:
            quiz = Quiz.objects.all()
            quiz_serializer = QuizSerializer(quiz, many=True)
            return GenericSuccessResponse(quiz_serializer.data, message=QUIZ_FETCHED_SUCCESSFULLY)
        except Exception:
            return GenericException()

    @staticmethod
    def post(request):
        try:
            if not all(field in request.data for field in ["quiz_name", "description", "course"]):
                return CustomBadRequest(message=BAD_REQUEST)
            
            quiz_serializer = QuizSerializer(data=request.data)
            if quiz_serializer.is_valid(raise_exception=True):
                quiz = quiz_serializer.save()
                return GenericSuccessResponse(QuizSerializer(quiz).data, message=QUIZ_CREATED_SUCCESSFULLY)
        except Quiz.DoesNotExist:
            return GenericException(message='Quiz not found')
        except Exception:
            return GenericException()

    @staticmethod
    def patch(request):
        try:
            if "quiz_id" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)
            
            quiz = Quiz.objects.get(quiz_id=request.data['quiz_id'])
            quiz_serializer = QuizSerializer(quiz, data=request.data, partial=True)
            if quiz_serializer.is_valid(raise_exception=True):
                quiz = quiz_serializer.save()
                return GenericSuccessResponse(QuizSerializer(quiz).data, message=QUIZ_UPDATED_SUCCESSFULLY)
        except Quiz.DoesNotExist:
            return GenericException(message='Quiz not found')
        except Exception:
            return GenericException()

    @staticmethod
    def delete(request):
        try:
            if "quiz_id" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)
            
            quiz = Quiz.objects.get(quiz_id=request.data['quiz_id'])
            quiz.delete()
            return GenericSuccessResponse(message=QUIZ_DELETED_SUCCESSFULLY)
        except Quiz.DoesNotExist:
            return GenericException(message='Quiz not found')
        except Exception:
            return GenericException()


class ManageQuestions(APIView):
    authentication_classes = [ProfessorJWTAuthentication]

    @staticmethod
    def get(request):
        try:
            questions = Questions.objects.all()
            questions_serializer = QuestionsSerializer(questions, many=True)
            return GenericSuccessResponse(questions_serializer.data, message=QUESTION_FETCHED_SUCCESSFULLY)
        except Exception:
            return GenericException()

    @staticmethod
    def post(request):
        try:
            required_fields = ["quiz_id", "question_type", "answer", "marks", "question"]
            if not all(field in request.data for field in required_fields):
                return CustomBadRequest(message=BAD_REQUEST)
            
            if request.data['question_type'] == "MCQ" and "options" not in request.data:
                return CustomBadRequest(message=OPTIONS_ARE_MISSING)
            
            if request.data['question_type'] == "TRUE_OR_FALSE" and request.data['answer'] not in ['True', 'False']:
                return CustomBadRequest(message=ANS_MUST_BE_TRUE_OR_FALSE)
            
            questions_serializer = QuestionsSerializer(data=request.data)
            quiz = Quiz.objects.get(quiz_id=request.data['quiz_id'])
            quiz.total_marks += int(request.data['marks'])
            
            if questions_serializer.is_valid(raise_exception=True):
                question = questions_serializer.save()
                quiz.save()
                return GenericSuccessResponse(QuestionsSerializer(question).data, message=QUESTION_CREATED_SUCCESSFULLY)
        except Quiz.DoesNotExist:
            return GenericException(message='Quiz not found')
        except Exception:
            return GenericException()

    @staticmethod
    def patch(request):
        try:
            if "question_id" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)
            
            question = Questions.objects.get(question_id=request.data["question_id"])
            
            if 'marks' in request.data:
                quiz = Quiz.objects.get(quiz_id=question.quiz_id.quiz_id)
                quiz.total_marks = quiz.total_marks - question.marks + int(request.data['marks'])
            
            if "question_type" in request.data:
                if request.data["question_type"] in ["ONE_WORD", "TRUE_OR_FALSE"]:
                    request.data['option'] = None

            update_questions_serializer = UpdateQuestionsSerializer(data=request.data)
            if update_questions_serializer.is_valid(raise_exception=True):
                question = update_questions_serializer.update(question, request.data)
                quiz.save()
                return GenericSuccessResponse(UpdateQuestionsSerializer(question).data, message=QUESTION_UPDATED_SUCCESSFULLY)
        except Exception:
            return GenericException()

    @staticmethod
    def delete(request):
        try:
            if "question_id" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)
            
            question = Questions.objects.get(question_id=request.data["question_id"])
            quiz = Quiz.objects.get(quiz_id=question.quiz_id.quiz_id)
            quiz.total_marks -= question.marks
            quiz.save()
            question.delete()
            return GenericSuccessResponse(message=QUESTION_DELETED_SUCCESSFULLY)
        except Exception:
            return GenericException()
