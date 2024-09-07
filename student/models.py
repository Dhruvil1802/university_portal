from django.db import models

from Admin.models import Courses
from quiz.models import Quiz
from resources.models import Assignment
from common.models import Audit

# Create your models here.
    
class Student(Audit):
    class Meta:
        db_table = 'up_student'

    student_id = models.BigAutoField(primary_key=True)
    student_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

class SubjectSelection(Audit):
    class Meta:
        db_table = 'up_subject_selection'

    subject_selection_id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    course = models.ForeignKey(Courses,on_delete=models.CASCADE)


class SubmitedAssignment(Audit):
    class Meta:
        db_table = 'up_submitedassignment'
    
    submited_assignment_id = models.BigAutoField(primary_key=True)
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE,default=None) 
    student = models.ForeignKey(Student,on_delete=models.CASCADE,default=None)
    assigned_marks = models.IntegerField(null=True)
    assignment_solution = models.FileField(upload_to='Files/assignmentsolutions', db_column="assignment_file", null=True, blank=True)
    course = models.ForeignKey(Courses,on_delete=models.CASCADE,default=None)

class QuizScore(Audit):
    class Meta:
        db_table = 'up_quiz_score'
    
    quizscore_id = models.BigAutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,default=None) 
    student = models.ForeignKey(Student,on_delete=models.CASCADE,default=None)
    marks_scored = models.IntegerField(null=True)
