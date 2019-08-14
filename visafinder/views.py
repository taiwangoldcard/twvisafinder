# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render


def home(request):
    return render(request, 'home.html', context={'support_email': settings.SUPPORT_EMAIL })
