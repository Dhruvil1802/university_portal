import re
import traceback
from django.shortcuts import render
from common.constants import (
    ASSIGNMENT_FETCHED_SUCCESSFULLY, ASSIGNMENT_IS_ALREADY_SUBMITTED, BAD_REQUEST,
    PASSWORD_LENGTH_SHOULD_BE_BETWEEN_8_TO_20, PASSWORD_MUST_HAVE_ONE_NUMBER,
    PASSWORD_MUST_HAVE_ONE_SMALLERCASE_LETTER, PASSWORD_MUST_HAVE_ONE_SPECIAL_CHARACTER,
    PASSWORD_MUST_HAVE_ONE_UPPERCASE_LETTER, QUESTION_FETCHED_SUCCESSFULLY,
    QUIZ_CREATED_SUCCESSFULLY, QUIZ_FETCHED_SUCCESSFULLY, QUIZ_GRADE_FETCHED_SUCCESSFULLY, SERIALIZER_IS_NOT_VALID, SUBJECT_DELETED, SUBJECT_FETCHED, SUBJECT_SELECTED,
    SUBMITED_ASSIGNMENT, TOTAL_MARKS_SAVED_SUCCESSFULLY, USER_IS_NOT_ENROLLED_IN_THIS_SUBJECT, USER_LOGGED_IN_SUCCESSFULLY, USER_LOGGED_OUT_SUCCESSFULLY,
    USER_REGISTERED_SUCCESSFULLY
)
from quiz.models import Questions, Quiz
from quiz.serializers import QuizSerializer
from student.models import (
    QuizScore, Student, SubjectSelection, SubmitedAssignment
)
from security.student_authorization import (
    StudentJWTAuthentication, get_student_authentication_token, save_token
)
from security.models import StudentAuthTokens
from exceptions.generic import CustomBadRequest, GenericException
from exceptions.generic_response import GenericSuccessResponse
from rest_framework.views import APIView

from django.db.models import Q
from student.serializers import (
    QuizTestSerializer, QuizTotalMarksSerializer, RegistrationSerializer,
    SubjectSelectionSerializer, SubmitedAssignmentSerializer, ViewGradeSerializer
)


class Registration(APIView):
    @staticmethod
    def post(request):
        try:
            if not all(key in request.data for key in ["password", "email", "student_name"]):
                return CustomBadRequest(message=BAD_REQUEST)

            password = request.data["password"]
            special_characters = r"[\$#@!\*]"

            if len(password) < 8 or len(password) > 20:
                return CustomBadRequest(message=PASSWORD_LENGTH_SHOULD_BE_BETWEEN_8_TO_20)
            if re.search('[0-9]', password) is None:
                return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_NUMBER)
            if re.search('[a-z]', password) is None:
                return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_SMALLERCASE_LETTER)
            if re.search('[A-Z]', password) is None:
                return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_UPPERCASE_LETTER)
            if re.search(special_characters, password) is None:
                return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_SPECIAL_CHARACTER)

            registration_serializer = RegistrationSerializer(data=request.data)

            if registration_serializer.is_valid(raise_exception=True):

                student = registration_serializer.save()
                tokens = get_student_authentication_token(student)
                save_token(tokens)

                return GenericSuccessResponse(tokens, message=USER_REGISTERED_SUCCESSFULLY)
            
            return CustomBadRequest(message=SERIALIZER_IS_NOT_VALID)

        except Exception:
            return GenericException()


class Logout(APIView):
    authentication_classes = [StudentJWTAuthentication]

    @staticmethod
    def delete(request):
        try:
            header = request.headers.get("authorization")
            if not header:

                return CustomBadRequest(message="Authorization header missing")

            token = header.split(" ")[1]
            StudentAuthTokens.objects.filter(Q(access_token=token) | Q(refresh_token=token)).delete()

            return GenericSuccessResponse(message=USER_LOGGED_OUT_SUCCESSFULLY)
        
        except Exception:
            return GenericException()


class Login(APIView):
    @staticmethod
    def post(request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")

            if not email or not password:
                raise GenericException(message="Email and password are required.")

            student = Student.objects.get(email=email, is_deleted=False)
            if password != student.password:
                raise GenericException(message="Incorrect password.")

            authentication_tokens = get_student_authentication_token(student)
            save_token(authentication_tokens)
            return GenericSuccessResponse(authentication_tokens, message=USER_LOGGED_IN_SUCCESSFULLY)

        except Student.DoesNotExist:
            raise GenericException(message="Email not found.")
        except Exception:
            return GenericException()


class ManageSubjects(APIView):
    authentication_classes = [StudentJWTAuthentication]
    @staticmethod
    def get(request):
        try:

            request.data["student"] = request.user.student_id
            courses = SubjectSelection.objects.filter(student = request.data['student'])
        

            return GenericSuccessResponse(SubjectSelectionSerializer(courses,many=True).data, message=SUBJECT_FETCHED)
        
        except SubjectSelection.DoesNotExist:
            raise GenericException(detail="Email not found")
        
        except Exception:
           
            return GenericException()

    @staticmethod
    def post(request):
        try:
            if "course" not in request.data:
                return CustomBadRequest(BAD_REQUEST)

            request.data["student"] = request.user.student_id
            subject_selection_serializer = SubjectSelectionSerializer(data=request.data)

            if subject_selection_serializer.is_valid(raise_exception=True):
                selected_subject = subject_selection_serializer.save()
                return GenericSuccessResponse(SubjectSelectionSerializer(selected_subject).data, message=SUBJECT_SELECTED)
        
        except Student.DoesNotExist:
            raise GenericException(detail="Email not found")
        except Exception:
            return GenericException()
    
    @staticmethod
    def delete(request):
        try:
            if "subject_id" not in request.data:
                return CustomBadRequest(BAD_REQUEST)
            request.data["student"] = request.user.student_id
            selected_subject = SubjectSelection.objects.get(course=request.data['subject_id'],student=request.data["student"] )
            selected_subject.delete()
        
            return GenericSuccessResponse(SubjectSelectionSerializer(selected_subject).data, message=SUBJECT_DELETED)
        
        except SubjectSelection.DoesNotExist:
            raise GenericException(message="Subject selection not found.")
        except Exception:
            return GenericException()


class SubmitAssignment(APIView):
    authentication_classes = [StudentJWTAuthentication]

    @staticmethod
    def post(request):
        try:
            
            if "assignment" not in request.data or "assignment_solution" not in request.data or "course" not in request.data :
                return CustomBadRequest(BAD_REQUEST)

            request.data["student"] = request.user.student_id

            if SubmitedAssignment.objects.filter(student=request.data["student"],assignment=request.data["assignment"]).exists():
                return CustomBadRequest(message=ASSIGNMENT_IS_ALREADY_SUBMITTED)
            
            if not SubjectSelection.objects.filter(student=request.data["student"],course=request.data["course"]):
                return CustomBadRequest(message=USER_IS_NOT_ENROLLED_IN_THIS_SUBJECT)
            
            submited_assignment_serializer = SubmitedAssignmentSerializer(data=request.data)

            if submited_assignment_serializer.is_valid(raise_exception=True):
                submitted_assignment = submited_assignment_serializer.save()
                return GenericSuccessResponse(SubmitedAssignmentSerializer(submitted_assignment).data, message=SUBMITED_ASSIGNMENT)
        
        except Student.DoesNotExist:
            raise GenericException(message="Student not found.")
        
        except Exception:
            return GenericException()


class ViewGrades(APIView):
    authentication_classes = [StudentJWTAuthentication]

    @staticmethod
    def get(request):
        try:
            assignments = SubmitedAssignment.objects.all()
            return GenericSuccessResponse(ViewGradeSerializer(assignments, many=True).data, message=ASSIGNMENT_FETCHED_SUCCESSFULLY)

        except SubmitedAssignment.DoesNotExist:
            return GenericException(message='Assignments not found')
        
        except Exception:
            return GenericException()


class GetQuiz(APIView):
    authentication_classes = [StudentJWTAuthentication]

    @staticmethod
    def get(request, course):
        try:
            student = request.user

            quiz_ids = Quiz.objects.filter(course=course).values_list("quiz_id", flat=True)
            taken_quizzes = QuizScore.objects.filter(student=student, quiz__in=quiz_ids).values_list("quiz", flat=True)
            quizzes = Quiz.objects.exclude(quiz_id__in=taken_quizzes).filter(quiz_id__in=quiz_ids)

            serializer = QuizSerializer(quizzes, many=True)
            return GenericSuccessResponse(serializer.data, message=QUIZ_FETCHED_SUCCESSFULLY)

        except Quiz.DoesNotExist:
            return GenericException(message='Quizzes not found')

        except Exception:
            
            return GenericException()


class GetQuestions(APIView):
    authentication_classes = [StudentJWTAuthentication]

    @staticmethod
    def get(request, quiz_id):
        try:
            questions = Questions.objects.filter(quiz_id=quiz_id)
            return GenericSuccessResponse(QuizTestSerializer(questions, many=True).data, message=QUESTION_FETCHED_SUCCESSFULLY)

        except Questions.DoesNotExist:
            return GenericException(message='Questions not found')
        
        except Exception:
            return GenericException()


class SubmitQuiz(APIView):
    authentication_classes = [StudentJWTAuthentication]

    @staticmethod
    def post(request):
        try:
            if "data" not in request.data:
                return CustomBadRequest(BAD_REQUEST)

            request.data["student"] = request.user.student_id

            total_marks = 0
            for i in request.data['data']:
                question = Questions.objects.get(question_id=i["question_id"])

                if i["selected_answer"] == question.answer:
                    total_marks += int(question.marks)
                request.data["quiz"] = question.quiz_id.quiz_id

            request.data["marks_scored"] = total_marks

            quiz_total_marks_serializer = QuizTotalMarksSerializer(data=request.data)

            if quiz_total_marks_serializer.is_valid(raise_exception=True):
                quiz = quiz_total_marks_serializer.save()
                return GenericSuccessResponse(QuizTotalMarksSerializer(quiz).data, message=TOTAL_MARKS_SAVED_SUCCESSFULLY)

        except Exception:
            return GenericException()



class QuizGrades(APIView):
    authentication_classes = [StudentJWTAuthentication]

    @staticmethod
    def get(request,course):
        try:
            student = request.user.student_id
           
            quiz = Quiz.objects.filter(course=course).values_list("quiz_id")
            quizscore = QuizScore.objects.filter(student=student,quiz__in=quiz)
            
            return GenericSuccessResponse(QuizTotalMarksSerializer(quizscore, many=True).data, message=QUIZ_GRADE_FETCHED_SUCCESSFULLY)

        except SubmitedAssignment.DoesNotExist:
            return GenericException(message='Assignments not found')
        
        except Exception:
            return GenericException()