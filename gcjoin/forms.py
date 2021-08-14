from django import forms

from .models import GoldCardHolder

import math
import re


ID_REGEX = '^[A-Z]{1}[1-2A-D8-9]{1}[0-9]{8}$';
ID_LETTERS = 'ABCDEFGHJKLMNPQRSTUVXYWZIO';



class GCJoinForm(forms.ModelForm):
    #TODO add validation for ARC ID number
    class Meta:
        model = GoldCardHolder
        fields = ['name', 'dob', 'identityno', 'nation', 'email', 'line', 'job', 'intro',
                  'needs', 'directory', 'newsletter', 'profile', 'wanttohelp',
                  'groups']
    def __init__(self, *args, **kwargs):
        super(GCJoinForm, self).__init__(*args, **kwargs)


    def isIDValid(id_no):
        id_no = id_no.upper()
        regex = re.compile(ID_REGEX)
        if (regex.match(id_no) is None):
                return False

        letterIndex = ID_LETTERS.index(id_no[0])
        checksum = math.floor(letterIndex / 10 + 1) + (letterIndex * 9)

        # Legacy ARC
        if (re.match('[A-Z]', id_no[1])):
                checksum = checksum + (ID_LETTERS.index(id_no[1]) % 10) * 8;
        else:
                checksum = checksum + int(id_no[1]) * 8

        for position in range(2, 9):
                checksum = checksum + (9 - position) * int(id_no[position])

        checksum = checksum + int(id_no[9])

        if (checksum % 10) == 0:
                return True
        else:
                return False
