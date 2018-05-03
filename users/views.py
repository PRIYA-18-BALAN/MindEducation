# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect

from messageotp import send_message
from users.forms import LoginForm, RegistrationForm
from users.models import Question, Worksheet, Answer, Option, OTP


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
            return redirect('verify_otp', user.id)
    return render(request, 'users/login.html', {'form': form})


def verify_otp(request, user_id):
    user = User.objects.get(id=user_id)
    otp = OTP.objects.get(user=user)
    if otp.verified:
        return redirect("profile")
    else:
        if request.method == 'POST':
            otp_num = request.POST.get("otp")
            if otp.otp == int(otp_num):
                otp.verified = True
                otp.save()
                messages.add_message(request, messages.SUCCESS, "OTP Verified Successfully")
                return redirect("profile")
            else:
                messages.error(request, "Wrong OTP")
        return render(request, 'users/verify_otp.html')


def registration(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            otp_num = random.randint(1000, 10000)
            otp = OTP.objects.create(user=user, otp=otp_num)
            send_message(
                "OTP for Mind Education System for user " + form.cleaned_data['username'] + " is " + str(otp_num))
            messages.success(request, "User Registered Successfully")
            return redirect('login')
    return render(request, 'users/registration.html', {'form': form})


@login_required
def profile_page(request):
    date_wise_points = []
    user = request.user
    date = datetime.now() - timedelta(days=30)
    max = 0
    doc_link = "https://www.sriramakrishnahospital.com/doctor/ananth-s/"
    max_count = 0
    for i in range(0, 31):
        points = user.answered_questions.filter(question__type=0, created_at__date=date.date()).aggregate(
            Sum('question__point'))['question__point__sum']
        if not points:
            points = 0
        temp = \
            user.answered_questions.filter(question__type=1, created_at__date=date.date()).aggregate(
                Sum('option__point'))[
                'option__point__sum']
        if temp:
            points += temp
        date_wise_points.append({'date': date.date().strftime("%d-%m-%Y"), 'points': points})
        if max < points:
            max = points
        if points > 2:
            max_count += 1
        date = date + timedelta(days=1)
        if max_count >= 5:
            return render(request, 'users/profile.html',
                          {'date_wise_points': date_wise_points, 'max': max, 'doc_link': doc_link})
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


def test(request):
    data = request.GET.get("data", None)
    if data:
        return HttpResponse("Received " + str(data))
    return HttpResponse("Success")
