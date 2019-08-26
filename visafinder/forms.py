from django import forms
from django_countries import countries
from django_countries.widgets import CountrySelectWidget


class VisaSearchForm(forms.Form):
        country = forms.ChoiceField(widget=CountrySelectWidget, choices=countries)
