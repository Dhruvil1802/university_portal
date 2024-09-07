import datetime
from django.shortcuts import render
from django.db.models import Q

from common.constants import SERIALIZER_IS_NOT_VALID, TOKEN_IS_EXPIRED
from professor.models import Professor
from security.serializers import ProfessorAuthTokenSerializer
from exceptions.generic import CustomBadRequest, GenericException
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
import jwt

from django.conf import settings
from security.models import ProfessorAuthTokens


def get_professor_authentication_token(professor):
    professor_refresh_token = jwt.encode(
        payload={
            "token_type": "refresh",
            "professor_id": professor.professor_id,
            "email": professor.email,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + settings.REFRESH_TOKEN_LIFETIME
        },
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    professor_access_token = jwt.encode(
        payload={
            "token_type": "access",
            "professor_id": professor.professor_id,
            "email": professor.email,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + settings.ACCESS_TOKEN_LIFETIME
        },
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return {
        "professor_access_token": professor_access_token,
        "professor_refresh_token": professor_refresh_token
    }


def save_token(token):
    professor_auth_token_serializer = ProfessorAuthTokenSerializer(
        data={
            "access_token": token["professor_access_token"],
            "refresh_token": token["professor_refresh_token"]
        }
    )

    if professor_auth_token_serializer.is_valid():
        professor_auth_token_serializer.save()
    else:
        raise CustomBadRequest(message=SERIALIZER_IS_NOT_VALID)


class ProfessorJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            header = request.headers.get("authorization")
            if not header:
                return CustomBadRequest(message="Authorization header missing")

            professor_token = header.split(" ")[1]

            if not ProfessorAuthTokens.objects.filter(Q(access_token=professor_token) | Q(refresh_token=professor_token)).exists():
                return CustomBadRequest(message=TOKEN_IS_EXPIRED)

            claims = jwt.decode(professor_token, key=settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            professor = Professor.objects.get(professor_id=claims["professor_id"], email=claims["email"], is_deleted=False)

            return professor, claims

        except Professor.DoesNotExist:
            raise   GenericException(message = "Professor does not exist")
        except Exception:
            raise GenericException()
