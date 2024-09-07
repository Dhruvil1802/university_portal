import datetime
from django.shortcuts import render
from django.db.models import Q
from Admin.models import Administrator

from common.constants import SERIALIZER_IS_NOT_VALID, TOKEN_IS_EXPIRED
from security.serializers import AdminAuthTokenSerializer
from exceptions.generic import CustomBadRequest, GenericException
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
import jwt

from django.conf import settings
from security.models import AdminAuthTokens


def get_admin_authentication_token(admin):
    admin_refresh_token = jwt.encode(
        payload={
            "token_type": "refresh",
            "admin_id": admin.admin_id,
            "email": admin.email,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + settings.REFRESH_TOKEN_LIFETIME
        },
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    admin_access_token = jwt.encode(
        payload={
            "token_type": "access",
            "admin_id": admin.admin_id,
            "email": admin.email,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + settings.ACCESS_TOKEN_LIFETIME
        },
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return {
        "admin_access_token": admin_access_token,
        "admin_refresh_token": admin_refresh_token
    }


def save_token(token):
    admin_auth_token_serializer = AdminAuthTokenSerializer(
        data={
            "access_token": token["admin_access_token"],
            "refresh_token": token["admin_refresh_token"]
        }
    )

    if admin_auth_token_serializer.is_valid():
        admin_auth_token_serializer.save()
    else:
        raise CustomBadRequest(message=SERIALIZER_IS_NOT_VALID)


class AdminJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            header = request.headers.get("authorization")
            if not header:
                return CustomBadRequest(message="Authorization header missing")

            admin_token = header.split(" ")[1]

            if not AdminAuthTokens.objects.filter(Q(access_token=admin_token) | Q(refresh_token=admin_token)).exists():
                return CustomBadRequest(message=TOKEN_IS_EXPIRED)

            claims = jwt.decode(admin_token, key=settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            admin = Administrator.objects.get(admin_id=claims["admin_id"], email=claims["email"], is_deleted=False)

            return admin, claims

        except Administrator.DoesNotExist:
            raise GenericException(message ="Admin does not exist")
        except Exception:
            raise GenericException()

