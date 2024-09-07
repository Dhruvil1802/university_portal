from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

class AdminAuthTokens(models.Model):
    class Meta:
        db_table = 'up_admin_auth_tokens'

    access_token = models.TextField(null=True, db_column="auth_access_token")
    refresh_token = models.TextField(null=True, db_column="auth_refresh_token")
    created_at = models.DateTimeField(auto_now_add=True)

class ProfessorAuthTokens(models.Model):
    class Meta:
        db_table = 'up_professor_auth_tokens'

    access_token = models.TextField(null=True, db_column="auth_access_token")
    refresh_token = models.TextField(null=True, db_column="auth_refresh_token")
    created_at = models.DateTimeField(auto_now_add=True)

class StudentAuthTokens(models.Model):
    class Meta:
        db_table = 'up_student_auth_tokens'

    access_token = models.TextField(null=True, db_column="auth_access_token")
    refresh_token = models.TextField(null=True, db_column="auth_refresh_token")
    created_at = models.DateTimeField(auto_now_add=True)