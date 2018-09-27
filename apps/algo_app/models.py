from __future__ import unicode_literals
from django.db import models
from apps.login_app.models import User
import re

class Lesson(models.Model):
    number = models.IntegerField()
    subject = models.CharField(max_length=255)
    instructions = models.TextField()

class Sub_lesson(models.Model):
    number = models.IntegerField()
    category = models.CharField(max_length=255)
    instructions = models.TextField()
    lessons = models.ForeignKey(Lesson, related_name="sub_lessons")

class Answer(models.Model):
    regex = models.TextField()
    lessons = models.ManyToManyField(Lesson, related_name="answers")
    sub_lessons = models.ManyToManyField(Sub_lesson, related_name="answers")
