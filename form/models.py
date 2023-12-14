from django.db import models


class Student(models.Model):
    fullname = models.CharField(max_length=255)
    course = models.IntegerField()
    study_org = models.CharField(max_length=255)
    email = models.EmailField()
    telegram = models.CharField(max_length=255)
