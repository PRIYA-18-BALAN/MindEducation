# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Worksheet(models.Model):
    name = models.CharField(max_length=500)
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
      return self.name

class Question(models.Model):
    QUIZ = 0
    QUESTION = 1
    TYPE_CHOICE = ((QUIZ, 'Quiz'), (QUESTION, 'Question'))
    quiz = models.ForeignKey(Worksheet, related_name='questions')
    question = models.TextField()
    type = models.IntegerField(choices=TYPE_CHOICE, default=QUESTION)
    point = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
     return self.question

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='choices')
    text = models.CharField(max_length=500)
    point = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
      return self.text

class Answer(models.Model):
    user = models.ForeignKey(User, related_name='answered_questions')
    question = models.ForeignKey(Question, related_name='answers')
    answer = models.TextField(null=True,blank=True)
    option = models.ForeignKey(Option, related_name='chosen_answers',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
      return self.user+ " "+ self.question
