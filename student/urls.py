from django.urls import path
from .views import  GetQuestions, GetQuiz, Login, Logout, ManageSubjects, QuizGrades, Registration, SubmitAssignment, SubmitQuiz, ViewGrades
#,  OTPVerification, ResetPassword, ForgotPassword, AllHolidays

app_name = "student"

urlpatterns = [

    path("registration/", Registration.as_view()),

    path("logout/", Logout.as_view()),

    path("login/", Login.as_view()),

    path("managesubjects/",ManageSubjects.as_view()),

    path("submitassignment/",SubmitAssignment.as_view()),

    path('viewgrades/', ViewGrades.as_view()),

    path('getquestions/<int:quiz_id>/', GetQuestions.as_view()),

    path('submitquiz/', SubmitQuiz.as_view()),

    path('getquiz/<int:course>/', GetQuiz.as_view()),

    path('quizgrades/<int:course>/', QuizGrades.as_view()),
   
]   
