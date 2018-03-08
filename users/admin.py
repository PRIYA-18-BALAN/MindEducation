# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from users.models import *

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Option)
admin.site.register(Worksheet)
