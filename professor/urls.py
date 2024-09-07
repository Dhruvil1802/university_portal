from django.urls import path
from .views import  Login, Logout, Registration
#,  OTPVerification, ResetPassword, ForgotPassword, AllHolidays

app_name = "professor"

urlpatterns = [
    path("registration/", Registration.as_view()),

    path("logout/", Logout.as_view()),

    path("login/", Login.as_view()),
]