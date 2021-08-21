# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.conf import settings
from django.shortcuts import get_object_or_404, render
import json
import math
import re
import requests
from .models import GoldCardHolder
from .forms import GCJoinForm

# Set to OFFLINE to disable the call to the NIA API.
MODE = "ONLINE"


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def validate_goldcard(identityno, nation, dob):
    """ uses the NIA API to verify whether a Gold Card is valid
        identityno is an ARC number
        nation is an integer that matches the NIA list of countries
        dob is a string like 1970-01-01

        Returns True if ID is valid, a string with an error if not"""
    if GCJoinForm.isIDValid(identityno) is False:
        return "Invalid ID number"

    try:
        datetime.strptime(str(dob), '%Y-%m-%d')
    except ValueError:
        return "Invalid Date of Birth"

    if MODE == "ONLINE":
        r = requests.get('https://coa.immigration.gov.tw/coa-frontend/golden-card/re-apply/inquiry?residentIdNo='+ identityno + '&birthDate=' + str(dob).replace('-', '/') + '&grace=0')
    else:
        rr = {}
        rr["status_code"] = 200
        rr["text"] = '{"nation":208}'
        r = dotdict(rr)

    if r.status_code != 200:
       return "HTTP error on NIA API."

    results = json.loads(r.text)
    print(results)

    if 'nation' in results.keys():
        if results["nation"] == nation:
            # We have a valid Gold Card holder!
            return True
        else:
            return "Valid ID with invalid country. " + r.text

    else:
        return "Not valid Gold Card information, failed verification. " + r.text

def join(request):
    if request.method == 'POST':
        # TODO - restrict number of POSTS based on IP address.
        form = GCJoinForm(request.POST)
        if form.is_valid():
            print(request.POST)
            new_goldie = form.save()
            if GCJoinForm.isIDValid(new_goldie.identityno) is False:
               new_goldie.notes = "Invalid ARC Number."
               new_goldie.save()
               return render(request, 'gcerror.html', context={
                  'support_email': settings.SUPPORT_EMAIL,
                  'status_code': 200,
                  'message': "Invalid ARC Number."
                    })

            validation_result = validate_goldcard(new_goldie.identityno, new_goldie.nation, new_goldie.dob)
            if validation_result is True:
               new_goldie.status = 'Approved'
               new_goldie.save()
               # TODO: Automatically add to LINE group
               # TODO: Automatically invite to slack group
               # TODO: Automatically add to newsletter list
               return render(request, 'success.html', context={
                   'support_email': settings.SUPPORT_EMAIL,
                    })
            else:
               new_goldie.notes = validation_result
               new_goldie.save()
               return render(request, 'gcerror.html', context={
                  'support_email': settings.SUPPORT_EMAIL,
                  'status_code': 401,
                  'message': validation_result,
                    })

        else:
            # Form Validation failed
            return render(request, 'gcerror.html', context={
              'support_email': settings.SUPPORT_EMAIL,
              'status_code': 401,
              'message': form.errors
                })

    else:
        # It's a GET request!
        form = GCJoinForm()
        return render(request, 'join.html', context={
            'support_email': settings.SUPPORT_EMAIL,
            'gcjoinform': form,
             })
