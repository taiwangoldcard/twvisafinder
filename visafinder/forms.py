from django import forms
from django_countries import countries
from django_countries.widgets import CountrySelectWidget

SCHOOL_LEVEL_CHOICES = [
    ('University', 'University'),
    ('High School', 'High School'),
]

VISIT_CHOICES = [
    ('Holiday', 'Holiday'),
    ('Visiting Family or Friends', 'Visiting Family or Friends'),
    ('Working Holiday', 'Working Holiday'),
    ('Attending a Conference or Expo', 'Attending a Conference or Expo'),
    ('Business Activities', 'Business Activities'),
    ('Medical Treatment', 'Medical Treatment'),
]

class VisaSearchForm(forms.Form):
        country = forms.ChoiceField(widget=CountrySelectWidget, choices=countries)

        def __init__(self, *args, **kwargs):
            category = kwargs.pop('category')
            super(VisaSearchForm, self).__init__(*args, **kwargs)

            #if category == "Study":
            #    self.fields["School_Level"] = forms.ChoiceField(required=False, choices=SCHOOL_LEVEL_CHOICES, widget=forms.RadioSelect)
