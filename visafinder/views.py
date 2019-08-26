# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render
from visafinder.models import VisaCategory
from visafinder.models import Visa

def home(request):
    # show the list of visa categories
    return render(request, 'home.html', context={
        'support_email': settings.SUPPORT_EMAIL,
        'categories': VisaCategory.objects.all(),
        })

def category(request, visa_category):
    # show results within a category, or a form with additional information to get a results
    matched_categories = VisaCategory.objects.filter(name=visa_category)
    if len(matched_categories) == 1:
        visas = matched_categories[0].visa_set.all()
        return render(request, 'category.html', context={
            'support_email': settings.SUPPORT_EMAIL,
            'category': matched_categories[0].name,
            'visas': visas,
             })
    else:
        return render(request, 'home.html', context={
            'support_email': settings.SUPPORT_EMAIL,
            'categories': VisaCategory.objects.all(),
            })

def result(request):
    # show personalised results based on the input
    return render(request, 'result.html', context={'support_email': settings.SUPPORT_EMAIL })

def visa(request, visa):
    # show the information we have about a particular visa
    print(visa)
    print(Visa.objects.all())
    matched_visas = Visa.objects.filter(name=visa)
    if len(matched_visas) == 1:
        return render(request, 'visa.html', context={
            'support_email': settings.SUPPORT_EMAIL,
            'visa': matched_visas[0],
             })
    else:
        return render(request, 'home.html', context={
            'support_email': settings.SUPPORT_EMAIL,
            'categories': VisaCategory.objects.all(),
            })

