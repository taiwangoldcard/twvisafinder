# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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


def join(request):
    print(request.method)
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
            if MODE == "ONLINE":
                r = requests.get('https://coa.immigration.gov.tw/coa-frontend/golden-card/re-apply/inquiry?residentIdNo='+ new_goldie.identityno + '&birthDate=' + str(new_goldie.dob).replace('-', '/') + '&grace=0')
            else:
                rr = {}
                rr["status_code"] = 200
                rr["text"] = '{"nation":208}'
                r = dotdict(rr)

            if r.status_code != 200:
               new_goldie.notes = "HTTP error on NIA API."
               new_goldie.save()
               return render(request, 'error.html', context={
                  'support_email': settings.SUPPORT_EMAIL,
                  'status_code': r.status_code,
                  'message': r.text
                    })
            results = json.loads(r.text)
            print(results)
            if 'nation' in results.keys():
                if results["nation"] == new_goldie.nation:
                    # We have a valid Gold Card holder!
                    new_goldie.status = 'Approved'
                    new_goldie.save()
                    # TODO: Automatically add to LINE group
                    # TODO: Automatically invite to slack group
                    # TODO: Automatically add to newsletter list
                    return render(request, 'success.html', context={
                        'support_email': settings.SUPPORT_EMAIL,
                         })
                else:
                    new_goldie.notes = "Valid ID with invalid country."
                    new_goldie.save()
                    return render(request, 'gcerror.html', context={
                      'support_email': settings.SUPPORT_EMAIL,
                      'status_code': r.status_code,
                      'message': "We couldn't match your country to the one on file."
                        })

            else:
                # Not valid Gold Card information
                return render(request, 'gcerror.html', context={
                  'support_email': settings.SUPPORT_EMAIL,
                  'status_code': r.status_code,
                  'message': r.text + "\nPlease email tw.goldcard@gmail.com with a copy of your Gold Card (you may blank personal details)"
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
