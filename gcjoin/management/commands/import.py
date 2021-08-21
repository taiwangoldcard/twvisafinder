#!/usr/bin/env python3

import csv
from datetime import datetime
from gcjoin.models import GoldCardHolder, GoldCardSubGroup
from django.core.management import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **kwargs):
        with open(kwargs['filename'], 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                newgoldie, created = GoldCardHolder.objects.get_or_create(
                    name = row['Name'],
                    status = 'Unknown',
                    joined_date = datetime.strptime(row['Timestamp'], '%m/%d/%Y %H:%M:%S'),
                    email = row['Email'],
                    line = row['Your Line ID (our community is a Line Group)'],
                    job = row['Previous/Current Job and Industry'],
                    intro = row['A quick introduction about you? (will be used to introduce you to the community)'],
                    needs = row['What are you looking for from the Community?'],
                    directory = True if row['Do you want to appear in the Gold Card Community Directory? Only your First name and first letter of your last name, industry, and intro appears. Other Gold Card Holders will only be able to contact you via Line only.  You\'ll be able to change the informations provided'] == 'Yes' else False,
                    newsletter = True if row['Do you want to receive email regarding the Gold Card Community (events, news, regulations changes etc...) ?'] == 'Yes' else False,
                    profile = True if row['Do you want to be interviewed and your profile appear on taiwangoldcard.com?'] == 'Yes' else False,
                    wanttohelp = True if row['Would you be interested in helping the gold card the community? (any type of contributions is welcome: events/code/marketing/ideas...)'] == 'Yes' else False,
                    notes = "Imported by script",
                    )
                newgoldie.save()
                for group in row['Do you identify yourself in one of those groups? (you\'ll be invited)'].split(','):
                    group = group.strip()
                    subgroup = GoldCardSubGroup.objects.filter(title=group)
                    if len(subgroup) == 1:
                        newgoldie.groups.add(subgroup[0])
                    elif group != '':
                        print(group + " - group not found")

                newgoldie.save()
                GoldCardHolder.objects.filter(email=row['Email']).update(joined_date = datetime.strptime(row['Timestamp'], '%m/%d/%Y %H:%M:%S'))
