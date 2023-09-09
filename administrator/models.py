from django.db import models
from .choices import QUESTION_TYPES

# Create your models here.

class ExamDetails(models.Model):
    exam_id = models.CharField(max_length=100, unique=True)
    exam_type = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    created_date = models.DateField(auto_now_add=True)

class Questions(models.Model):
    exam = models.ForeignKey(ExamDetails, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    mark = models.IntegerField()
    question_type = models.IntegerField(choices=QUESTION_TYPES)
    created_date = models.DateField(auto_now_add=True)


class Answers(models.Model):
    answers = models.CharField(max_length=100, null=True)
    is_correct = models.BooleanField(null=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, null=True)