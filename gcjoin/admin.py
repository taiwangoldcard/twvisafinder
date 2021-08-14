# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import GoldCardHolder, GoldCardSubGroup, GoldCardRole

admin.site.register(GoldCardHolder)
admin.site.register(GoldCardSubGroup)
admin.site.register(GoldCardRole)
