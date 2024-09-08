import traceback
from django.shortcuts import render
from resources.models import ProfsAnnouncements, Assignment, Notes
from resources.serializers import CheckAssignmentSerializer, ProfsAnnouncementSerializer, AssignmentSerializer, NotesSerializer
from common.constants import (ANNOUNCEMENT_DELETED_SUCCESSFULLY, ANNOUNCEMENT_FETCHED_SUCCESSFULLY, ANNOUNCEMENT_POSTED_SUCCESSFULLY, ANNOUNCEMENT_UPDATED_SUCCESSFULLY, 
                              ASSIGNMENT_CHECKED_SUCCESSFULLY, ASSIGNMENT_CREATED_SUCCESSFULLY, 
                              ASSIGNMENT_DELETED_SUCCESSFULLY, ASSIGNMENT_FETCHED_SUCCESSFULLY, 
                              ASSIGNMENT_UPDATED_SUCCESSFULLY, BAD_REQUEST, SERIALIZER_IS_NOT_VALID)
from exceptions.generic import CustomBadRequest, GenericException
from exceptions.generic_response import GenericSuccessResponse
from rest_framework.views import APIView
from security.professor_authorization import ProfessorJWTAuthentication
from student.models import SubmitedAssignment
from student.serializers import SubmitedAssignmentSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class PostAssignment(APIView):
    authentication_classes = [ProfessorJWTAuthentication]

    parser_classes = (MultiPartParser, FormParser, JSONParser)
    @staticmethod
    def post(request):
        try:
            if "assignment_name" not in request.data or "assignment_description" not in request.data or 'assignment_question_file' not in request.data or 'marks' not in request.data or 'course' not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)
            
            assignment_serializer = AssignmentSerializer(data=request.data)
            
            if assignment_serializer.is_valid(raise_exception=True):
                assignment = assignment_serializer.save()
                return GenericSuccessResponse(AssignmentSerializer(assignment).data, message=ASSIGNMENT_CREATED_SUCCESSFULLY)

        except Exception:
            return GenericException()

    parser_classes = (MultiPartParser, FormParser, JSONParser)
    @staticmethod
    def patch(request):
        try:
            if "assignment_name" not in request.data or "assignment_description" not in request.data or 'assignment_question_file' not in request.data or 'marks' not in request.data or "assignment_id" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)
            
            assignment = Assignment.objects.get(assignment_id=request.data['assignment_id'])
            assignment_serializer = AssignmentSerializer(assignment, data=request.data)

            if assignment_serializer.is_valid(raise_exception=True):
                assignment = assignment_serializer.save()
                return GenericSuccessResponse(AssignmentSerializer(assignment).data, message=ASSIGNMENT_UPDATED_SUCCESSFULLY)
            
        except Assignment.DoesNotExist:
            return GenericException(message='Course not found.')
        except Exception:
            return GenericException()

    parser_classes = (MultiPartParser, FormParser, JSONParser)
    @staticmethod
    def delete(request):
        try:
            if "assignment_id" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)
            
            assignment = Assignment.objects.get(assignment_id=request.data['assignment_id'])
            assignment.delete()

            return GenericSuccessResponse(AssignmentSerializer(assignment).data, message=ASSIGNMENT_DELETED_SUCCESSFULLY)

        except Assignment.DoesNotExist:
            return GenericException(message='Course not found.')       
        except Exception:
            return GenericException()

    @staticmethod
    def get(request):
        try:
            assignment = Assignment.objects.all()
            return GenericSuccessResponse(AssignmentSerializer(assignment, many=True).data, message=ASSIGNMENT_FETCHED_SUCCESSFULLY)
        except Assignment.DoesNotExist:
            return GenericException(message='Course not found.')
        except Exception:
            return GenericException()


class PostNotes(APIView):
    authentication_classes = [ProfessorJWTAuthentication]

    parser_classes = (MultiPartParser, FormParser, JSONParser)
    @staticmethod
    def post(request):
        try:
            if "notes_name" not in request.data or "notes_description" not in request.data or 'notes_content' not in request.data or 'course' not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)
            
            notes_serializer = NotesSerializer(data=request.data)
            
            if notes_serializer.is_valid(raise_exception=True):
                notes = notes_serializer.save()
                return GenericSuccessResponse(NotesSerializer(notes).data, message=ASSIGNMENT_CREATED_SUCCESSFULLY)
            
        except Exception:
            
            return GenericException()

    parser_classes = (MultiPartParser, FormParser, JSONParser)
    @staticmethod
    def patch(request):
        try:
            if  "notes_id" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)
            
            notes = Notes.objects.get(notes_id=request.data['notes_id'])
            notes_serializer = NotesSerializer(notes, data=request.data)

            if notes_serializer.is_valid(raise_exception=True):
                notes = notes_serializer.save()
                return GenericSuccessResponse(NotesSerializer(notes).data, message=ASSIGNMENT_UPDATED_SUCCESSFULLY)
        except Notes.DoesNotExist:
            return GenericException(message='notes not found.')   
        except Exception:
           
            return GenericException()

    parser_classes = (MultiPartParser, FormParser, JSONParser)
    @staticmethod
    def delete(request):
        try:
            if "notes_id" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)
            
            notes = Notes.objects.get(notes_id=request.data['notes_id'])
            notes.delete()

            return GenericSuccessResponse(NotesSerializer(notes).data, message=ASSIGNMENT_DELETED_SUCCESSFULLY)

        except Notes.DoesNotExist:
            return GenericException(message='Course not found.')              
        except Exception:
            return GenericException()

    @staticmethod
    def get(request):
        try:
            notes = Notes.objects.all()
            return GenericSuccessResponse(NotesSerializer(notes, many=True).data, message=ASSIGNMENT_FETCHED_SUCCESSFULLY)
        except Notes.DoesNotExist:
            return GenericException(message='Course not found.')            
        except Exception:
            return GenericException()


class Announcement(APIView):
    authentication_classes = [ProfessorJWTAuthentication]

    @staticmethod
    def get(request):
        try:
            announcements = ProfsAnnouncements.objects.all()
            return GenericSuccessResponse(ProfsAnnouncementSerializer(announcements, many=True).data, message=ANNOUNCEMENT_FETCHED_SUCCESSFULLY)
       
        except ProfsAnnouncements.DoesNotExist:
            return GenericException(message='Announcements not found')
        
        except Exception:
            return GenericException()

    @staticmethod
    def post(request):
        try:
            if "description" not in request.data or "topic" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)
            
            profsannouncement_serializer = ProfsAnnouncementSerializer(data=request.data)

            if profsannouncement_serializer.is_valid(raise_exception=True):
                announcement = profsannouncement_serializer.save()
                return GenericSuccessResponse(ProfsAnnouncementSerializer(announcement).data, message=ANNOUNCEMENT_POSTED_SUCCESSFULLY)

        except ProfsAnnouncements.DoesNotExist:                                             
            return GenericException(message='Announcement not found.')
        except Exception:
            
            return GenericException()

    @staticmethod
    def patch(request):
        try:
            if "announcement_id" not in request.data:
                return GenericException(message=BAD_REQUEST)
            
            announcement = ProfsAnnouncements.objects.get(announcement_id=request.data['announcement_id'])
            announcement_serializer = ProfsAnnouncementSerializer(announcement, data=request.data, partial=True)
            
            if announcement_serializer.is_valid(raise_exception=True):
                announcement = announcement_serializer.save()
                return GenericSuccessResponse(ProfsAnnouncementSerializer(announcement).data, message=ANNOUNCEMENT_UPDATED_SUCCESSFULLY)
            else:
                return GenericException(message=SERIALIZER_IS_NOT_VALID)
        
        except ProfsAnnouncements.DoesNotExist:
            return GenericException(message='Announcement not found.')

        except Exception:
            traceback.print_exc()
            return GenericException()

    @staticmethod
    def delete(request):
        try:
            if "announcement_id" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)
            
            announcement = ProfsAnnouncements.objects.get(announcement_id=request.data['announcement_id'])
            announcement.delete()  
            return GenericSuccessResponse(ProfsAnnouncementSerializer(announcement).data, message=ANNOUNCEMENT_DELETED_SUCCESSFULLY)

        except ProfsAnnouncements.DoesNotExist:
            return GenericException(message='Announcement not found')
        except Exception:
            return GenericException()


class CheckAssignment(APIView):
    authentication_classes = [ProfessorJWTAuthentication]

    @staticmethod
    def get(request):
        try:
            assignments = SubmitedAssignment.objects.all()
            return GenericSuccessResponse(SubmitedAssignmentSerializer(assignments, many=True).data, message=ASSIGNMENT_FETCHED_SUCCESSFULLY)

        except SubmitedAssignment.DoesNotExist:
            return GenericException(message='Assignment not found')
        
        except Exception:
            return GenericException()

    @staticmethod
    def patch(request):
        try:
            if "submited_assignment_id" not in request.data or "assigned_marks" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)
            
            assignments = SubmitedAssignment.objects.get(submited_assignment_id=request.data["submited_assignment_id"])
            check_assignment_serializer = CheckAssignmentSerializer(assignments, data=request.data)

            if check_assignment_serializer.is_valid(raise_exception=True):
                assignments = check_assignment_serializer.save()
            return GenericSuccessResponse(CheckAssignmentSerializer(assignments).data, message=ASSIGNMENT_CHECKED_SUCCESSFULLY)

        except SubmitedAssignment.DoesNotExist:
            return GenericException(message='Assignment not found')
        
        except Exception:
            return GenericException()
