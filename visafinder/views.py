# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Visa, VisaCategory, VisaEligibility
from .forms import VisaSearchForm

def searchvisas(category, country):
    # finds the set of visas for which someone from this country is eligible

    # ignore visa eligibilities that expired, get those that apply to the specific country or all countries
    eligibilities = VisaEligibility.objects.filter(Q(country=country) | Q(all_countries=True),
                                                   Q(end_date__gte=date.today()) | Q(end_date=None))

    # now, filter out those not in the category and append to a list
    visas = []
    for eligibility in eligibilities:
        if category in eligibility.eligiblevisa.category.all():
            visas.append(eligibility.eligiblevisa)
    return visas

def home(request):
    # show the list of visa categories
    return render(request, 'home.html', context={
        'support_email': settings.SUPPORT_EMAIL,
        'categories': VisaCategory.objects.all(),
        })

def category(request, visa_category):
    # show results within a category, or a form with additional information to get a results
    category = get_object_or_404(VisaCategory, name=visa_category)

    if request.method == 'POST':
        form = VisaSearchForm(request.POST, category=visa_category)
        if form.is_valid():
            visas = searchvisas(category, form.cleaned_data['country'])
            print visas
            #visas = category.visa_set.all()
            return render(request, 'category.html', context={
                'support_email': settings.SUPPORT_EMAIL,
                'category': category.name,
                'visas': visas,
                 })
    else:
        form = VisaSearchForm(category=category.name)
        visas = category.visa_set.all()
        return render(request, 'category.html', context={
            'support_email': settings.SUPPORT_EMAIL,
            'category': category.name,
            'visas': visas,
            'visasearchform': form,
             })

def result(request):
    # show personalised results based on the input
    return render(request, 'result.html', context={'support_email': settings.SUPPORT_EMAIL })

def visa(request, visa):
    # show the information we have about a particular visa
    visa = get_object_or_404(Visa, name=visa)
    return render(request, 'visa.html', context={
        'support_email': settings.SUPPORT_EMAIL,
        'visa': visa,
         })
