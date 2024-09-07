# Generated by Django 5.0.2 on 2024-09-04 15:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('assignment_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('assignment_name', models.CharField(max_length=255)),
                ('assignment_description', models.CharField(max_length=255)),
                ('assignment_question_file', models.FileField(blank=True, db_column='assignment_file', null=True, upload_to='Assignments/assignment_question')),
                ('marks', models.IntegerField()),
                ('course', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Admin.courses')),
            ],
            options={
                'db_table': 'up_assignment',
            },
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('notes_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('notes_name', models.CharField(max_length=255)),
                ('notes_description', models.CharField(max_length=255)),
                ('notes_content', models.FileField(blank=True, db_column='assignment_file', null=True, upload_to='notes')),
                ('course', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Admin.courses')),
            ],
            options={
                'db_table': 'up_notes',
            },
        ),
        migrations.CreateModel(
            name='ProfsAnnouncements',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('announcement_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('topic', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=10000)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.courses')),
            ],
            options={
                'db_table': 'up_profsannouncements',
            },
        ),
    ]
