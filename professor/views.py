import re
from common.constants import (
    BAD_REQUEST,
    PASSWORD_LENGTH_SHOULD_BE_BETWEEN_8_TO_20,
    PASSWORD_MUST_HAVE_ONE_NUMBER,
    PASSWORD_MUST_HAVE_ONE_SMALLERCASE_LETTER,
    PASSWORD_MUST_HAVE_ONE_SPECIAL_CHARACTER,
    PASSWORD_MUST_HAVE_ONE_UPPERCASE_LETTER,
    SERIALIZER_IS_NOT_VALID,
    USER_LOGGED_IN_SUCCESSFULLY,
    USER_LOGGED_OUT_SUCCESSFULLY,
    USER_REGISTERED_SUCCESSFULLY
)
from professor.serializers import RegistrationSerializer
from professor.models import Professor
from security.professor_authorization import (
    ProfessorJWTAuthentication,
    get_professor_authentication_token,
    save_token
)
from security.models import ProfessorAuthTokens
from exceptions.generic import CustomBadRequest, GenericException
from exceptions.generic_response import GenericSuccessResponse
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError
from django.db.models import Q


class Registration(APIView):
    @staticmethod
    def post(request):
        try:
            if not all(field in request.data for field in ["password", "email", "professor_name"]):
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
                professor = registration_serializer.save()
                tokens = get_professor_authentication_token(professor)
                save_token(tokens)
                return GenericSuccessResponse(tokens, message=USER_REGISTERED_SUCCESSFULLY)
            
            return CustomBadRequest(message=SERIALIZER_IS_NOT_VALID)

        except Exception:
            return GenericException()


class Logout(APIView):
    authentication_classes = [ProfessorJWTAuthentication]

    @staticmethod
    def delete(request):
        try:
            header = request.headers.get("authorization")
            if not header:
                return CustomBadRequest(message="Authorization header missing")

            token = header.split(" ")[1]
            ProfessorAuthTokens.objects.filter(
                Q(access_token=token) | Q(refresh_token=token)
            ).delete()

            return GenericSuccessResponse(message=USER_LOGGED_OUT_SUCCESSFULLY)

        except Exception:
            return GenericException()


class Login(APIView):
    def post(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")

            if not email or not password:
                raise GenericException(message="Email and password are required.")

            professor = Professor.objects.get(email=email, is_deleted=False)
            if password != professor.password:
                raise GenericException(message="Incorrect password.")

            authentication_tokens = get_professor_authentication_token(professor)
            save_token(authentication_tokens)
            return GenericSuccessResponse(authentication_tokens, message=USER_LOGGED_IN_SUCCESSFULLY)

        except Professor.DoesNotExist:
            raise NotFound(detail="Email not found.")
        except Exception:
            return GenericException()
