# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Sum
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
            return redirect('login')
    return render(request, 'users/registration.html', {'form': form})


@login_required
def profile_page(request):
    date_wise_points = []
    user = request.user
    date = datetime.now() - timedelta(days=30)
    max = 0
    for i in range(0, 31):
        points = user.answered_questions.filter(question__type=1, created_at__date=date.date()).aggregate(
            Sum('question__point'))['question__point__sum']
        if not points:
            points = 0
        temp = \
            user.answered_questions.filter(question__type=2, created_at__date=date.date()).aggregate(
                Sum('option__point'))[
                'option__point__sum']
        if temp:
            points += temp
        date_wise_points.append({'date': date.date().strftime("%d-%m-%Y"), 'points': points})
        if max < points:
            max = points
        date = date + timedelta(days=1)
    return render(request, 'users/profile.html', {'date_wise_points': date_wise_points, 'max': max})


@login_required
def questions_list(request):
    worksheets = Worksheet.objects.all()
    data = []
    for worksheet in worksheets:
        dict_data = {'questions': [], 'name': worksheet.name}
        flag = False
        date = datetime.now().date()
        for question in worksheet.questions.filter(~Q(answers__created_at__date=date, answers__user=request.user)):
            flag = True
            dict_data['questions'].append(question)
        if flag:
            data.append(dict_data)
    return render(request, 'users/worksheet_list.html', {'data': data})


@login_required
def question_view(request, id):
    question = Question.objects.get(id=id)
    if request.method == 'POST':
        answer = request.POST.get("answer")
        if answer:
            if question.type == 0:
                option = Option.objects.get(id=answer)
                Answer.objects.create(user=request.user, question=question, option=option)
            else:
                Answer.objects.create(user=request.user, question=question, answer=request.POST.get('answer'))
            messages.success(request, 'Response Recorded')
            return redirect('questions_list')
        else:
            messages.info(request, 'Please Enter a valid Answer')
    return render(request, 'users/question_view.html', {'question': question})


def user_manual(request):
    return render(request, 'users/user_manual.html')
