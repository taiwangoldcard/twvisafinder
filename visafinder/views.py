# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render


def home(request):
    # show the list of visa categories
    return render(request, 'home.html', context={'support_email': settings.SUPPORT_EMAIL })

def category(request):
    # show results within a category, or a form with additional information to get a results
    return render(request, 'home.html', context={'support_email': settings.SUPPORT_EMAIL })

def result(request):
    # show personalised results based on the input
    return render(request, 'home.html', context={'support_email': settings.SUPPORT_EMAIL })

def visa(request):
    # show the information we have about a particular visa
    return render(request, 'visa.html', context={'support_email': settings.SUPPORT_EMAIL })


