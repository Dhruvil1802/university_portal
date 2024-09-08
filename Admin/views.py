import re
import traceback
from django.shortcuts import render
from requests import Response
from common.constants import (
    ANNOUNCEMENT_DELETED_SUCCESSFULLY,
    ANNOUNCEMENT_FETCHED_SUCCESSFULLY,
    ANNOUNCEMENT_POSTED_SUCCESSFULLY,
    ANNOUNCEMENT_UPDATED_SUCCESSFULLY,
    BAD_REQUEST,
    COURSE_ADDED_SUCCESSFULLY,
    COURSE_FETCHED_SUCCESSFULLY,
    COURSE_UPDATED_SUCCESSFULLY,
    PASSWORD_LENGTH_SHOULD_BE_BETWEEN_8_TO_20,
    PASSWORD_MUST_HAVE_ONE_NUMBER,
    PASSWORD_MUST_HAVE_ONE_SMALLERCASE_LETTER,
    PASSWORD_MUST_HAVE_ONE_SPECIAL_CHARACTER,
    PASSWORD_MUST_HAVE_ONE_UPPERCASE_LETTER,
    QUIZ_CREATED_SUCCESSFULLY,
    SERIALIZER_IS_NOT_VALID,
    USER_LOGGED_IN_SUCCESSFULLY,
    USER_LOGGED_OUT_SUCCESSFULLY,
    USER_REGISTERED_SUCCESSFULLY
)
from Admin.serializers import (
    AnnouncementSerializer,
    CourseSerializer,
    RegistrationSerializer
)
from Admin.models import Administrator, Announcements, Courses
from professor.models import Professor
from security.admin_authorization import AdminJWTAuthentication
from security.models import AdminAuthTokens
from security.admin_authorization import (
    AdminJWTAuthentication,
    get_admin_authentication_token,
    save_token
)
from exceptions.generic import BadRequest, CustomBadRequest, CustomNotFound, GenericException
from exceptions.generic_response import GenericSuccessResponse
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError
from django.db.models import Q


class Registration(APIView):
    
    @staticmethod
    def post(request):
        try:
            if "password" not in request.data or "email" not in request.data or "admin_name" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)

            password = request.data["password"]
            special_characters = r"[\$#@!\*]"

            if len(password) < 8 or len(password) > 20:
                return CustomBadRequest(message=PASSWORD_LENGTH_SHOULD_BE_BETWEEN_8_TO_20)
            
            elif re.search('[0-9]', password) is None:
                return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_NUMBER)
            
            elif re.search('[a-z]', password) is None:
                return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_SMALLERCASE_LETTER)
            
            elif re.search('[A-Z]', password) is None:
                return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_UPPERCASE_LETTER)
            
            elif re.search(special_characters, password) is None:
                return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_SPECIAL_CHARACTER)

            registration_serializer = RegistrationSerializer(data=request.data)
            
            if registration_serializer.is_valid(raise_exception=True):
                admin = registration_serializer.save()
                tokens = get_admin_authentication_token(admin)
                save_token(tokens)
                return GenericSuccessResponse(tokens, message=USER_REGISTERED_SUCCESSFULLY)
            else:
                return CustomBadRequest(message=SERIALIZER_IS_NOT_VALID)

        except Administrator.DoesNotExist:
            raise GenericException(detail="user not found")
        
        except Exception as e:
            traceback.print_exc()
            return GenericException()


class Logout(APIView):
    authentication_classes = [AdminJWTAuthentication]

    @staticmethod
    def delete(request):
        try:
            header = request.headers.get("authorization")

            if not header:
                return CustomBadRequest(message=BAD_REQUEST)
            
            token = header.split(" ")[1]
            deletedtoken = AdminAuthTokens.objects.filter(Q(access_token=token) | Q(refresh_token=token)).delete()
        
            return GenericSuccessResponse(message=USER_LOGGED_OUT_SUCCESSFULLY)
        
        except Administrator.DoesNotExist:
            raise CustomNotFound()
        
        except Exception as e:
            return GenericException()


class Login(APIView):
    
    def post(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")

            if not email or not password:
                raise GenericException(message="Email and password are required.")
            
            customer = Administrator.objects.get(email=email, is_deleted=False)
            
            if not (password == customer.password):
                raise GenericException(message="Incorrect password")
            
            authentication_tokens = get_admin_authentication_token(customer)
            save_token(authentication_tokens)
            return GenericSuccessResponse(authentication_tokens, message=USER_LOGGED_IN_SUCCESSFULLY)
        
        except Administrator.DoesNotExist:
            raise GenericException(message="Email not found.")
        
        except Exception as e:
            return GenericException()


class ManageCourses(APIView):
    authentication_classes = [AdminJWTAuthentication]

    @staticmethod
    def get(request):
        try:
            courses = Courses.objects.all()
            return GenericSuccessResponse(CourseSerializer(courses, many=True).data, message=COURSE_FETCHED_SUCCESSFULLY)
        
        except Courses.DoesNotExist:
            return GenericException(message='Course not found')
        
        except Exception as e:
            traceback.print_exc()
            return GenericException()

    @staticmethod
    def post(request):
        try:
            if "course_name" not in request.data or "course_credit" not in request.data or "description" not in request.data or "course_faculty" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)

            course_serializer = CourseSerializer(data=request.data)

            if course_serializer.is_valid(raise_exception=True):
                course = course_serializer.save()
                return GenericSuccessResponse(CourseSerializer(course).data, message=COURSE_ADDED_SUCCESSFULLY)
        
        except Courses.DoesNotExist:
            return GenericException(message='Course not found.')
        
        except Exception as e:
            traceback.print_exc()
            return GenericException()

    @staticmethod
    def patch(request):
        try:
            if "course_id" not in request.data:
                return GenericException(message=BAD_REQUEST)
            
            course = Courses.objects.get(course_id=request.data['course_id'])
            
            if "professor" in request.data:
                professor = Professor.objects.get(professor_id=request.data['course_faculty'])
                request.data['course_faculty'] = professor
            
            course_serializer = CourseSerializer(course, data=request.data, partial=True)
            
            if course_serializer.is_valid():
                course = course_serializer.save()
                return GenericSuccessResponse(CourseSerializer(course).data, message=COURSE_UPDATED_SUCCESSFULLY)
            else:
                return GenericException(message=SERIALIZER_IS_NOT_VALID)
        
        except Courses.DoesNotExist:
            return GenericException(message='Course not found.')
        
        except Professor.DoesNotExist:
            return GenericException(message='Professor not found.')
        
        except Exception as e:
            traceback.print_exc()
            return GenericException()
    
    @staticmethod
    def delete(request):
        try:
            if "course_id" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)
            
            course = Courses.objects.get(course_id=request.data['course_id'])
            course.delete()
            
            return GenericSuccessResponse(CourseSerializer(course).data, message="Course deleted")
        
        except Courses.DoesNotExist:
            return GenericException(message='Course not found')
        
        except Exception as e:
            
            return GenericException()


class ManageAnnouncement(APIView):
    authentication_classes = [AdminJWTAuthentication]

    @staticmethod
    def get(request):
        try:
            announcements = Announcements.objects.all()
            return GenericSuccessResponse(AnnouncementSerializer(announcements, many=True).data, message=ANNOUNCEMENT_FETCHED_SUCCESSFULLY)
        
        except Announcements.DoesNotExist:
            return GenericException(message='Announcements not found.')
        
        except Exception as e:
            return GenericException(message='An unexpected error occurred.')

    @staticmethod
    def post(request):
        try:
            if "description" not in request.data or "topic" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)
            
            announcement_serializer = AnnouncementSerializer(data=request.data)

            if announcement_serializer.is_valid(raise_exception=True):
                announcement = announcement_serializer.save()
                return GenericSuccessResponse(AnnouncementSerializer(announcement).data, message=ANNOUNCEMENT_POSTED_SUCCESSFULLY)
        
        except Announcements.DoesNotExist:
            return GenericException(message='Announcement not found.')
        
        except Exception as e:
            traceback.print_exc()
            return GenericException()

    @staticmethod
    def patch(request):
        try:
            if "announcement_id" not in request.data:
                return GenericException(message=BAD_REQUEST)
            
            announcement = Announcements.objects.get(announcement_id=request.data['announcement_id'])
            announcement_serializer = AnnouncementSerializer(announcement, data=request.data, partial=True)
            
            if announcement_serializer.is_valid():
                announcement = announcement_serializer.save()
                return GenericSuccessResponse(AnnouncementSerializer(announcement).data, message=ANNOUNCEMENT_UPDATED_SUCCESSFULLY)
            else:
                return GenericException(SERIALIZER_IS_NOT_VALID)
        
        except Announcements.DoesNotExist:
            return GenericException(message='Announcement not found.')
        
        except Professor.DoesNotExist:
            return GenericException(message='Professor not found.')
        
        except Exception as e:
            traceback.print_exc()
            return GenericException()
    
    @staticmethod
    def delete(request):
        try:
            if "announcement_id" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)
            
            announcement = Announcements.objects.get(announcement_id=request.data['announcement_id'])
            announcement.delete()
            
            return GenericSuccessResponse(AnnouncementSerializer(announcement).data, message=ANNOUNCEMENT_DELETED_SUCCESSFULLY)
        
        except Announcements.DoesNotExist:
            return GenericException(message='Announcement not found')
        
        except Exception as e:
            traceback.print_exc()
            return GenericException()
