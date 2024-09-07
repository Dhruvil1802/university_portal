from django.urls import path

from resources.views import Announcement, CheckAssignment, PostAssignment, PostNotes
# from .views import  
#,  OTPVerification, ResetPassword, ForgotPassword, AllHolidays

app_name = "assignment"

urlpatterns = [

    path("postassignment/", PostAssignment.as_view()),
    path("postnotes/", PostNotes.as_view()),
    path("postannouncement/", Announcement.as_view()),
    path("checkassignment/", CheckAssignment.as_view()),
    
    
   
]