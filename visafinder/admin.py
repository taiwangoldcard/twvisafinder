# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Visa, VisaCategory, VisaEligibility

admin.site.register(Visa)
admin.site.register(VisaCategory)
admin.site.register(VisaEligibility)
