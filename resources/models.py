from django.db import models

from Admin.models import Courses
from common.models import Audit


# Create your models here.

class Assignment(Audit):
    class Meta:
        db_table='up_assignment'

    assignment_id = models.BigAutoField(primary_key=True)
    assignment_name = models.CharField(max_length=255)
    assignment_description = models.CharField(max_length=255)
    assignment_question_file = models.FileField(upload_to='Assignments/assignment_question', db_column="assignment_file", null=True, blank=True)
    marks = models.IntegerField()
    course = models.ForeignKey(Courses,on_delete=models.CASCADE,default=None)

class Notes(Audit):
    class Meta:
        db_table='up_notes'

    notes_id = models.BigAutoField(primary_key=True)
    notes_name = models.CharField(max_length=255)
    notes_description = models.CharField(max_length=255)
    notes_content =  models.FileField(upload_to='notes', db_column="assignment_file", null=True, blank=True)
    course = models.ForeignKey(Courses,on_delete=models.CASCADE,default=None)

class ProfsAnnouncements(Audit):
    class Meta:
        db_table = 'up_profsannouncements'

    announcement_id = models.BigAutoField(primary_key=True)
    topic = models.CharField(max_length=255)
    description = models.CharField(max_length=10000)
    course = models.ForeignKey(Courses,on_delete=models.CASCADE)

