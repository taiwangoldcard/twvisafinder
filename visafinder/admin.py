# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Visa, VisaCategory, VisaEligibility
from .models import GoldCardQualification, GoldCardQuestion

admin.site.register(Visa)
admin.site.register(VisaCategory)
admin.site.register(VisaEligibility)
admin.site.register(GoldCardQualification)
admin.site.register(GoldCardQuestion)
