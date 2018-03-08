from django.conf.urls import url

from users.views import *

urlpatterns = [
    url(r'^login', login_user, name='login'),
    url(r'^registration', registration, name='registration'),
    url(r'^profile', profile_page, name='profile'),
    url(r'^questions_list', questions_list, name='questions_list'),
    url(r'^question/(?P<id>[0-9]+)', question_view, name='question_view')
]
