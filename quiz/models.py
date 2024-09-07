from django.db import models
from enum import Enum

from Admin.models import Courses
from common.models import Audit

# Create your models here.
    
class QuestionType(Enum):
    MCQ = "mcq"
    ONE_WORD = "one word"
    TRUE_OR_FALSE = "true or false"
    
    @classmethod
    def choices(cls):
        return [(type.name, type.value) for type in cls]


 
class Quiz(Audit):
    class Meta:
        db_table = 'up_quiz'

    quiz_id = models.BigAutoField(primary_key=True)
    quiz_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    total_marks = models.IntegerField(default = 0)
    course = models.ForeignKey(Courses,on_delete=models.CASCADE,default=None) 

class Questions(Audit):
    class Meta:
        db_table = 'uq_Questions'
    
    question_id = models.BigAutoField(primary_key=True)
    question = models.CharField(max_length=255,null=True)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_type = models.CharField(choices=QuestionType.choices(), max_length=255,null=True)
    answer = models.CharField(max_length=255,null=True)
    options = models.CharField(max_length=255,null=True)
    marks = models.IntegerField(null=True)
    

