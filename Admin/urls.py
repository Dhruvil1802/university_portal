from django.urls import path
from .views import  Login, Logout, ManageAnnouncement, ManageCourses, Registration


app_name = "admin"

urlpatterns = [
    path("registration/", Registration.as_view()),

    path("logout/", Logout.as_view()),

    path("login/", Login.as_view()),

    path("managecourses/", ManageCourses.as_view()),

    path("manageannouncement/", ManageAnnouncement.as_view())
]