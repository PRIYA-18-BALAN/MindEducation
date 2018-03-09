# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect

from users.forms import LoginForm, RegistrationForm
from users.models import Question, Worksheet, Answer, Option


# Create your views here.


def landing_page(request):
    return render(request, 'users/base.html')


def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('profile')
    return render(request, 'users/login.html', {'form': form})


def registration(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User Registered Successfully")
            return redirect('profile')
    return render(request, 'users/registration.html', {'form': form})


@login_required
def profile_page(request):
    return render(request, 'users/profile.html')


@login_required
def questions_list(request):
    worksheets = Worksheet.objects.all()
    data = []
    for worksheet in worksheets:
        dict_data = {'questions': [], 'name': worksheet.name}
        flag = False
        for question in worksheet.questions.filter(~Q(answers__user=request.user)):
            flag = True
            dict_data['questions'].append(question)
        if flag:
            data.append(dict_data)
    return render(request, 'users/worksheet_list.html', {'data': data})


@login_required
def question_view(request, id):
    question = Question.objects.get(id=id)
    if request.method == 'POST':
        if question.type == 0:
            option = Option.objects.get(id=request.POST.get('answer'))
            Answer.objects.create(user=request.user, question=question, option=option)
        else:
            Answer.objects.create(user=request.user, question=question, answer=request.POST.get('answer'))
        messages.success(request, 'Response Recorded')
        return redirect('questions_list')
    return render(request, 'users/question_view.html', {'question': question})
