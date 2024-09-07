import datetime
from django.shortcuts import render
from django.db.models import Q

from common.constants import SERIALIZER_IS_NOT_VALID, TOKEN_IS_EXPIRED
from security.serializers import StudentAuthTokenSerializer
from exceptions.generic import CustomBadRequest, GenericException
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
import jwt

from django.conf import settings
from security.models import StudentAuthTokens
from student.models import Student


def get_student_authentication_token(student):
    student_refresh_token = jwt.encode(
        payload={
            "token_type": "refresh",
            "student_id": student.student_id,
            "email": student.email,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + settings.REFRESH_TOKEN_LIFETIME
        },
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    student_access_token = jwt.encode(
        payload={
            "token_type": "access",
            "student_id": student.student_id,
            "email": student.email,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + settings.ACCESS_TOKEN_LIFETIME
        },
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return {
        "student_access_token": student_access_token,
        "student_refresh_token": student_refresh_token
    }


def save_token(token):
    student_auth_token_serializer = StudentAuthTokenSerializer(
        data={
            "access_token": token["student_access_token"],
            "refresh_token": token["student_refresh_token"]
        }
    )

    if student_auth_token_serializer.is_valid():
        student_auth_token_serializer.save()
    else:
        raise CustomBadRequest(message=SERIALIZER_IS_NOT_VALID)


class StudentJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            header = request.headers.get("authorization")
            if not header:
                return CustomBadRequest(message="Authorization header missing")

            student_token = header.split(" ")[1]

            if not StudentAuthTokens.objects.filter(
                Q(access_token=student_token) | Q(refresh_token=student_token)
            ).exists():
                return CustomBadRequest(message=TOKEN_IS_EXPIRED)

            claims = jwt.decode(student_token, key=settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            student = Student.objects.get(
                student_id=claims["student_id"],
                email=claims["email"],
                is_deleted=False
            )

            return student, claims

        except Student.DoesNotExist:
            raise GenericException(message ="Student does not exist")
        except Exception:
            raise GenericException()
