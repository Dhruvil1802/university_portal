from django.db import models
from common.models import Audit

# Create your models here.
    
class Professor(Audit):
    class Meta:
        db_table = 'up_professor'

    professor_id = models.BigAutoField(primary_key=True)

    professor_name = models.CharField(max_length=255)

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=255)




