from django.db import models
from common.models import Audit
from professor.models import Professor

# Create your models here.

class Administrator(Audit):
    class Meta:
        db_table = 'up_administrator'

    admin_id = models.BigAutoField(primary_key=True)
    admin_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)


class Courses(Audit):
    class Meta:
        db_table = 'up_courses'
    
    course_id = models.BigAutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    course_credit = models.IntegerField(default=3)
    description = models.CharField(max_length=255)
    course_faculty = models.ForeignKey(Professor, on_delete=models.CASCADE, default=None)


class Announcements(Audit):
    class Meta:
        db_table = 'up_announcements'

    announcement_id = models.BigAutoField(primary_key=True)
    topic = models.CharField(max_length=255)
    description = models.CharField(max_length=10000)
