# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models
from django.core.exceptions import ValidationError

STATUS_CHOICES = [
    ('Pending', 'Pending Approval'),
    ('Approved', 'Verified as a Gold Card Holder'),
    ('Joined', 'Community Onboarding Complete'),
    ('Banned', 'Removed for being disruptive'),
    ('Unknown', 'Added before this system existed'),
    ('Rejected', 'Rejected'),
    ('Alumni', 'No longer holder of a valid Gold Card'),
]

COUNTRY_CHOICES = [
    (1, 'AFGHANISTAN'),
    (201, 'ALBANIA'),
    (501, 'ALGERIA'),
    (202, 'ANDORRA'),
    (548, 'ANGOLA'),
    (416, 'ANTIGUA AND BARBUDA'),
    (401, 'ARGENTINA'),
    (240, 'ARMENIA'),
    (471, 'ARUBA'),
    (101, 'AUSTRALIA'),
    (203, 'AUSTRIA'),
    (249, 'AZERBAIJAN'),
    (301, 'BAHAMAS'),
    (545, 'BAHRAIN'),
    (50, 'BANG LADESH'),
    (302, 'BARBADOS'),
    (206, 'BELARUS'),
    (204, 'BELGIUM'),
    (604, 'BELIZE'),
    (509, 'BENIN'),
    (2, 'BHUTAN'),
    (402, 'BOLIVIA'),
    (554, 'BOPHUTHATSWANA'),
    (254, 'BOSNIA'),
    (502, 'BOTSWANA'),
    (882, 'BOUVET ISLAND'),
    (403, 'BRAZIL'),
    (564, 'BRITISH INDIAN OCEAN TERRITORY'),
    (395, 'BRITISH VIRGIN ISLANDS'),
    (3, 'BRUNEI'),
    (205, 'BULGARIA'),
    (542, 'BURKINA FASO'),
    (4, 'BURMA'),
    (503, 'BURUNDI'),
    (5, 'CAMBODIA'),
    (505, 'CAMEROON'),
    (303, 'CANADA'),
    (551, 'CAPE VERDE'),
    (473, 'CAYMAN ISLANDS'),
    (504, 'CENTRAL AFRICAN'),
    (506, 'CHAD'),
    (404, 'CHILE'),
    (120, 'CHRISTMAS ISLAND'),
    (556, 'CISKEI'),
    (119, 'COCOS ISLANDS'),
    (405, 'COLOMBIA'),
    (396, 'COLON'),
    (553, 'COMOROS'),
    (507, 'CONGO'),
    (114, 'COOK ISLANDS'),
    (304, 'COSTA RICA'),
    (516, 'COTE D\'IVOIRE'),
    (251, 'CROATIA'),
    (305, 'CUBA'),
    (7, 'CYPRUS'),
    (207, 'CZECH REPUBLIC'),
    (208, 'DENMARK'),
    (552, 'DJIBOUTI'),
    (417, 'DOMINICA'),
    (306, 'DOMINICAN'),
    (93, 'DUBAI'),
    (406, 'ECUADOR'),
    (541, 'EGYPT'),
    (307, 'EL SALVADOR'),
    (510, 'EQUATORIAL GUINEA'),
    (546, 'ERITREA'),
    (239, 'ESTONIA'),
    (511, 'ETHIOPIA'),
    (474, 'FALKLAND ISLANDS'),
    (260, 'FAROE ISLANDS'),
    (102, 'FIJI'),
    (209, 'FINLAND'),
    (210, 'FRANCE'),
    (419, 'FRENCH GUIANA'),
    (881, 'FRENCH SOUTHERN TERRITORIES'),
    (512, 'GABON'),
    (513, 'GAMBIA'),
    (250, 'GEORGIA'),
    (237, 'GERMAN DEMOCRATIC'),
    (211, 'GERMANY'),
    (514, 'GHANA'),
    (212, 'GREECE(HELLENIC)'),
    (261, 'GREENLAND'),
    (326, 'GRENADA'),
    (475, 'GUADELOUPE'),
    (308, 'GUATEMALA'),
    (515, 'GUINEA'),
    (557, 'GUINEA BISSAU'),
    (407, 'GUYANA'),
    (309, 'HAITI'),
    (883, 'HEARD AND MCDONALD ISLANDS'),
    (213, 'HOLY SEE'),
    (310, 'HONDURAS'),
    (37, 'HONG KONG'),
    (214, 'HUNGARY'),
    (215, 'ICELAND'),
    (8, 'INDIA'),
    (9, 'INDONESIA'),
    (10, 'IRAN'),
    (11, 'IRAQ'),
    (216, 'IRELAND'),
    (12, 'ISRAEL'),
    (217, 'ITALY'),
    (311, 'JAMAICA'),
    (13, 'JAPAN'),
    (14, 'JORDAN'),
    (244, 'KAZAKHSTAN'),
    (517, 'KENYA'),
    (54, 'KIRIBATI'),
    (259, 'KOSOVO'),
    (16, 'KUWAIT'),
    (246, 'KYRGYZSTAN'),
    (17, 'LAOS'),
    (238, 'LATVIA'),
    (18, 'LEBANON'),
    (518, 'LESOTHO'),
    (519, 'LIBERIA'),
    (520, 'LIBYA'),
    (218, 'LIECHTENSTEIN'),
    (242, 'LITHUANIA'),
    (219, 'LUXEMBOURG'),
    (95, 'MACAO'),
    (253, 'MACEDONIA'),
    (521, 'MADAGASCAR'),
    (61, 'MAIN LAND AREA'),
    (522, 'MALAWI'),
    (19, 'MALAYSIA'),
    (20, 'MALDIVES'),
    (523, 'MALI'),
    (220, 'MALTA'),
    (327, 'MARSHALL'),
    (477, 'MARTINIQUE'),
    (524, 'MAURITANIA'),
    (525, 'MAURITIUS'),
    (565, 'MAYOTTE'),
    (312, 'MEXICO'),
    (194, 'MICRONESIAN'),
    (245, 'MOLDOVA'),
    (221, 'MONACO'),
    (21, 'MONGOLIA'),
    (257, 'MONTENEGRO'),
    (476, 'MONTSERRAT'),
    (526, 'MOROCCO'),
    (547, 'MOZAMBIQUE'),
    (560, 'NAMIBIA'),
    (103, 'NAURU'),
    (22, 'NEPAL'),
    (222, 'NETHERLANDS'),
    (472, 'NETHERLANDS ANTILLES'),
    (122, 'NEW CALEDONIA'),
    (104, 'NEW ZEALAND'),
    (313, 'NICARAGUA'),
    (527, 'NIGER'),
    (528, 'NIGERIA'),
    (115, 'NIUE'),
    (124, 'NORFOLK ISLAND'),
    (62, 'NORTH KOREA'),
    (33, 'NORTH YEMEN'),
    (121, 'NORTHERN MARIANA ISLANDS'),
    (223, 'NORWAY'),
    (53, 'OMAN'),
    (998, 'OTHER'),
    (23, 'PAKISTAN'),
    (92, 'PALESTINE'),
    (314, 'PANAMA'),
    (236, 'PAPUA NEW GUINEA'),
    (409, 'PARAGUAY'),
    (410, 'PERU'),
    (24, 'PHILIPPINES'),
    (127, 'PITCAIRN ISLANDS'),
    (224, 'POLISH'),
    (128, 'POLYNESIE'),
    (225, 'PORTUGAL'),
    (25, 'QATAR'),
    (35, 'REPUBLIC OF CHINA(TAIWAN)'),
    (196, 'REPUBLIC OF PALAU'),
    (563, 'REPUBLIC OF SOUTH SUDAN'),
    (226, 'ROMANIA'),
    (241, 'RUSSIAN'),
    (530, 'RWANDA'),
    (555, 'SAHARAUI'),
    (566, 'SAINT HELENA'),
    (602, 'SAINT LUCIA'),
    (601, 'SAINT VINCENT'),
    (227, 'SAN MARINO'),
    (558, 'SAO TOME &amp; PRINCIPE'),
    (26, 'SAUDI ARABIA'),
    (531, 'SENEGAL'),
    (258, 'SERBIA'),
    (55, 'SEYCHELLES'),
    (532, 'SIERRA LEONE'),
    (27, 'SINGAPORE'),
    (256, 'SLOVAK REPUBLIC'),
    (252, 'SLOVENIA'),
    (60, 'SOLOMON'),
    (533, 'SOMALIA'),
    (534, 'SOUTH AFRICA'),
    (478, 'SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS'),
    (15, 'SOUTH KOREA'),
    (28, 'SOUTH YEMEN'),
    (228, 'SPAIN'),
    (6, 'SRI LANKA'),
    (603, 'ST. CHRISTOPHER'),
    (479, 'ST.PIERRE AND MIQUELON'),
    (999, 'STATELESS'),
    (535, 'SUDAN'),
    (411, 'SURINAME'),
    (262, 'SVALBARD AND JAN MAYEN ISLANDS'),
    (536, 'SWAZILAND'),
    (229, 'SWEDEN'),
    (230, 'SWITZERLAND'),
    (29, 'SYRIAN ARAB'),
    (247, 'TAJIKISTAN'),
    (537, 'TANZANIA'),
    (30, 'THAILAND'),
    (562, 'THE REPUBLIC OF CONGO'),
    (31, 'TIMOR'),
    (538, 'TOGOLESE REPUBLIC'),
    (125, 'TOKELAU'),
    (106, 'TONGA'),
    (559, 'TRANSKEI'),
    (412, 'TRINIDAD'),
    (539, 'TUNISIA'),
    (32, 'TURKEY'),
    (248, 'TURKMEN'),
    (480, 'TURKS AND CAICOS ISLANDS'),
    (56, 'TUVALU'),
    (315, 'U S A'),
    (233, 'U S S R'),
    (540, 'UGANDA'),
    (231, 'UKRAINE'),
    (59, 'UNITED ARAB'),
    (232, 'UNITED KINGDOM'),
    (126, 'UNITED SATAES MINOR OUTLYING ISLANDS'),
    (408, 'URUGUAY'),
    (243, 'UZBEKISTAN'),
    (113, 'VANUATU'),
    (192, 'VANUATU'),
    (550, 'VENDA'),
    (413, 'VENEZUELA'),
    (34, 'VIETNAM'),
    (481, 'VIRGIN ISLANDS OF UNITED STATES'),
    (123, 'WALLIS AND FUTUNA ISLANDS'),
    (107, 'WESTERN SAMOA'),
    (801, 'WESTERN SAMOA'),
    (63, 'YEMEN'),
    (234, 'YUGOSLAVIA'),
    (508, 'ZAIRE'),
    (543, 'ZAMBIA'),
    (529, 'ZIMBABWE'),
]

class GoldCardRole(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=255)

    def __str__(self):
        return self.title


class GoldCardSubGroup(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.title


class GoldCardHolder(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(choices=STATUS_CHOICES, default="Pending", max_length=64)
    joined_date = models.DateField(auto_now_add=True, blank=True)
    identityno = models.CharField(max_length=12, verbose_name="Your Gold Card ID (ARC) number")
    dob = models.DateField(default=datetime.date(1970,1,1), verbose_name="Date of Birth", help_text="YYYY-MM-DD")
    nation = models.IntegerField(choices=COUNTRY_CHOICES, null=True)
    email = models.CharField(max_length=255)
    alt_email = models.CharField(max_length=255, blank=True, null=True, verbose_name="Alternate Email")
    line = models.CharField(max_length=255, blank=True, null=True, verbose_name="Your LINE ID", help_text="our community is a LINE Group")
    job = models.CharField(max_length=255, verbose_name="Previous/Current Job and Industry")
    intro = models.TextField(max_length=1024, verbose_name="A quick introduction about you?", help_text="will be used to introduce you to the community")
    needs = models.TextField(max_length=1024, blank=True, null=True, verbose_name="What are you looking for from the Community?")
    directory = models.BooleanField(verbose_name="Do you want to appear in the Gold Card Community Directory?", help_text="Only your First name and first letter of your last name, industry, and intro appears. Other Gold Card Holders will only be able to contact you via Line only. You'll be able to change the informations provided")
    newsletter = models.BooleanField(verbose_name="Do you want to receive email regarding the Gold Card Community?", help_text=" events, news, regulations changes etc...")
    profile = models.BooleanField(verbose_name="Do you want to be interviewed and your profile appear on taiwangoldcard.com?")
    wanttohelp = models.BooleanField(verbose_name="Would you be interested in helping the gold card the community?", help_text="any type of contributions is welcome: events/code/marketing/ideas...)")
    groups = models.ManyToManyField(GoldCardSubGroup, verbose_name="Do you identify yourself in one of those groups?", help_text="you'll be invited", blank=True)
    roles = models.ManyToManyField(GoldCardRole, blank=True)
    notes = models.TextField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # TODO reject duplicate emails/IDs
        if self.dob > (datetime.date.today() - datetime.timedelta(18*365)):
            raise ValidationError("Date of Birth Error: Only Adults may join this community")
        super(GoldCardHolder, self).save(*args, **kwargs)
