# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ast
from datetime import date
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Visa, VisaCategory, VisaEligibility
from .models import GoldCardQuestion, GoldCardQualification
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
            print(visas)
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

def goldcardqualification(request):
    # show the initial list of Gold Card qualification questions, or direct to
    # the next tree of questions.
    if request.method == 'POST':
        print (request.POST)
        enabled_trees = []
        # this is a post from the home screen.
        if "enabled_trees" not in request.POST.keys():
            for key in request.POST.keys():
                if key.isdigit():
                    enabled_trees.append(int(key))
            qualdata = []
            if 9 in enabled_trees:
               qualdata.append('9-0')
            if 12 in enabled_trees:
               qualdata.append('12-0')
               enabled_trees.remove(12)

        else:
            # XXX should make sure the webserver limits the request size.
            enabled_trees = ast.literal_eval(request.POST["enabled_trees"])
            qualdata = ast.literal_eval(request.POST["qualdata"])
            for key in request.POST.keys():
                parts = key.split('-')
                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                    qualdata.append(key)


        if len(enabled_trees) == 0:
            # either user did not select any of the top-level requirements, or
            # they are done.
            # we get qualdata like this: [u'2-1', u'7-2', u'9-1', u'9-2']
            # now to convert into ministry-article pairings.
            results = []
            for qual in qualdata:
                tree, order = qual.split('-')
                results.extend(GoldCardQuestion.objects.get(tree_id=tree, tree_order=order).qualifications.all())
            print (results)

            return render(request, 'goldcardqualificationresults.html', context={
                'support_email': settings.SUPPORT_EMAIL,
                'qualdata': results
                })
        else:
            enabled_trees.sort()
            start_tree = enabled_trees[0]
            enabled_trees.pop(0)
            start_questions = GoldCardQuestion.objects.filter(tree_id=start_tree)
            # By default, we follow the next tree information in the questions.
            # However, if a user selects many top-level trees, this would
            # result in skipping trees they enabled. Look at the enabled trees
            # and override the next tree if necessary.
            pointer_question = start_questions.filter(next_tree_id__isnull=False)
            if len(pointer_question) == 1:
                next_tree = pointer_question[0].next_tree_id
                if next_tree not in enabled_trees:
                    enabled_trees.append(next_tree)
                    enabled_trees.sort()
                for potential_tree in enabled_trees:
                    if next_tree > potential_tree:
                        next_tree = potential_tree
                        break
            else:
                next_tree = None


            # TODO need to pass qualifications
            return render(request, 'goldcardqualificationtree.html', context={
                'support_email': settings.SUPPORT_EMAIL,
                'questions': start_questions,
                'next_tree': next_tree,
                'enabled_trees': enabled_trees,
                'qualdata': qualdata,
                })


    else:
        return render(request, 'goldcardqualification.html', context={
            'support_email': settings.SUPPORT_EMAIL,
            'questions': GoldCardQuestion.objects.filter(tree_order=0),
            })

def goldcardqualificationtree(request, tree_id):
    # show one tree of Gold Card qualification questions
    return render(request, 'goldcardqualificationtree.html', context={
        'support_email': settings.SUPPORT_EMAIL,
        'questions': GoldCardQuestion.objects.filter(tree_id=tree_id),
        })

def goldcardqualificationresults(request):
    # show one tree of Gold Card qualification questions
    return render(request, 'goldcardqualificationresults.html', context={
        'support_email': settings.SUPPORT_EMAIL,
        'results': qualdata,
        })

