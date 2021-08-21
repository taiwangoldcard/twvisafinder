# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib import messages

from .models import GoldCardHolder, GoldCardSubGroup, GoldCardRole
from .views import validate_goldcard

@admin.action(description="Verify as Gold Card Holder")
def verify_GoldCardHolder(modeladmin, request, queryset):
    for goldie in queryset:
        if goldie.nation is None or goldie.identityno is None:
            modeladmin.message_user(request, goldie.name + " is missing details and can't be verified.", 'error')
            continue

        if validate_goldcard(goldie.identityno, goldie.nation, goldie.dob) is True:
            goldie.status='Approved'
            goldie.save()
            modeladmin.message_user(request, goldie.name + " was verified.")
        else:
            modeladmin.message_user(request, goldie.name + " could not be verified", 'error')

class GoldCardHolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'joined_date')
    actions = [verify_GoldCardHolder]

admin.site.register(GoldCardHolder, GoldCardHolderAdmin)
admin.site.register(GoldCardSubGroup)
admin.site.register(GoldCardRole)
