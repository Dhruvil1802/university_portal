from django.urls import path

from quiz.views import ManageQuestions, ManageQuiz

#,  OTPVerification, ResetPassword, ForgotPassword, AllHolidays

app_name = "student"

urlpatterns = [
    
    path("managequiz/", ManageQuiz.as_view()),

    path("managequestions/", ManageQuestions.as_view())

]