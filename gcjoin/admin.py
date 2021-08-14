# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import GoldCardHolder, GoldCardSubGroup, GoldCardRole

class GoldCardHolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'joined_date')

admin.site.register(GoldCardHolder, GoldCardHolderAdmin)
admin.site.register(GoldCardSubGroup)
admin.site.register(GoldCardRole)
