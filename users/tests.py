# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse

from users.models import Question, Answer, Worksheet, Option
# Create your tests here.
from users.views import login_user, registration, profile_page, question_view


class FullTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(first_name='Test', last_name='Test', username='Test')
        self.user.set_password('Test')
        self.user.save()
        self.worksheet = Worksheet.objects.create(name="Test", created_by=self.user)
        self.question_choice = Question.objects.create(quiz=self.worksheet, question="Test Question")
        self.question_without_choice = Question.objects.create(quiz=self.worksheet,
                                                               question="Test Question Without Choice",
                                                               point=5)
        self.choice = Option.objects.create(question=self.question_choice, text="Test Option", point=2)

    def test_answered_questions(self):
        Answer.objects.create(question=self.question_choice, user=self.user, option=self.choice)
        Answer.objects.create(question=self.question_without_choice, user=self.user, answer="Descriptive Answer")

        user = User.objects.get(username='Test')
        answers = user.answered_questions.all()
        for answer in answers:
            if answer.question.choices.exists():
                assert answer.option.text == 'Test Option'
            else:
                assert answer.answer == 'Descriptive Answer'

    def test_admin_login(self):
        request = self.factory.post('users/login', data={'username': 'Test', 'password': 'Test'})
        response = login_user(request)
        assert response.status_code == 302

    def test_register(self):
        request = self.factory.post('users/registration', data={
            'username': 'Srinath',
            'password': 'Srinath',
            'confirm_password': 'Srinath',
            'first_name': 'Srinath',
            'last_name': 'Srinath',
            'email': 'srinath.15cs@kct.ac.in'
        })
        response = registration(request)
        assert response.status_code == 302

    def test_profile_page(self):
        request = self.factory.post(reverse('profile'))
        request.user = AnonymousUser()
        response = profile_page(request)
        assert response.status_code != 200
        request.user = User.objects.get(username='Test')
        response = profile_page(request)
        assert response.status_code == 200

    def test_user_descriptive_answer(self):
        request = self.factory.post('users/question/' + str(self.question_without_choice.id),
                                    data={'answer': 'Test Answer'})
        request.user = self.user
        response = question_view(request, self.question_without_choice.id)
        assert response.status_code == 302

    def test_user_option_answer(self):
        request = self.factory.post('users/question/' + str(self.question_choice.id),
                                    data={'answer': self.choice.id})
        request.user = self.user
        response = question_view(request, self.question_choice.id)
        assert response.status_code == 302
