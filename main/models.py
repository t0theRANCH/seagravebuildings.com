from django.db import models
from django.contrib.auth.models import User

EMPTY_SELECTION = (('', '--Please Select--'),)

YES_NO = (
    ('yes', 'Yes'),
    ('no', 'No')
)

ZONES = (
    ('commercial', 'Commercial'),
    ('residential', 'Residential'),
    ('agricultural', 'Agricultural'),
    ('industrial', 'Industrial'),
    ('other', 'Other')
)

PURPOSE = (
    ('garage', 'Garage'),
    ('home', 'Home'),
    ('shed', 'Shed'),
    ('workshop', 'Workshop'),
    ('warehouse', 'Warehouse/Storage'),
    ('repair', 'Repair/Mechanic Shop'),
    ('agriculture', 'Agriculture'),
    ('retail', 'Retail Store'),
    ('factory', 'Factory/Assembly'),
    ('office', 'Office Space'),
    ('aviation', 'Aviation'),
    ('other', 'Other')
)

PROPERTY = (
    ('own', 'We own the property'),
    ('identified_financed', 'Identified property and arranged financing'),
    ('identified', 'Identified property, not financed'),
    ('no', 'No')
)

TIMELINE = (
    ('asap', 'ASAP'),
    ('1_3_months', '1-3 Months'),
    ('3_6_months', '3-6 Months'),
    ('6_12_months', '6-12 Months'),
    ('year', 'Over 1 year')
)

STYLE = (
    ('gable', 'Straight wall style (gable)'),
    ('monoslope', 'Straight wall style (single slope)'),
    ('quonset', 'Arch style (Quonset)')
)

INSULATION_ROOF = (
    ('2_inch', 'Yes - 2" thick'),
    ('4_inch', 'Yes - 4" thick'),
    ('6_inch', 'Yes - 6" thick'),
    ('no', 'No')
)

INSULATION_WALL = (
    ('2_inch', 'Yes - 2" thick'),
    ('4_inch', 'Yes - 4" thick'),
    ('no', 'No')
)

COLOUR = (
    ('standard', 'All Standard Colour Building'),
    ('galv_roof', 'Galvalume Roof, Standard Colour Walls'),
    ('all_galv', 'All Galvalume Building')
)


GUTTERS = (
    ('both', 'Yes, Both Sidewalls'),
    ('fs', 'Yes, Front Sidewall Only'),
    ('bs', 'Yes, Back Sidewall Only'),
    ('no', 'No')
)


class NewUser(models.Model):
    username = models.CharField(max_length=50)
    password1 = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)


class VerifyAccount(models.Model):
    user_id = models.IntegerField()
    hash_code = models.CharField(max_length=200)
    is_verified = models.BooleanField()


class NavMenuItem(models.Model):
    text = models.CharField(max_length=200)
    url = models.URLField(null=True)
    is_dropdown = models.BooleanField()
    dropdown = models.CharField(max_length=200, null=True)


class Site(models.Model):
    complete = models.BooleanField()
    customer = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    start_date = models.DateField()


class Equipment(models.Model):
    owned = models.BooleanField()
    type = models.CharField(max_length=200)
    unit_num = models.IntegerField()
    mileage = models.IntegerField()
    last_service = models.IntegerField()
    last_inspection = models.DateField()
    site = models.ForeignKey(Site, on_delete=models.SET_DEFAULT, default="0")


class Blueprint(models.Model):
    file_name = models.CharField(max_length=100)
    file = models.FileField(upload_to='blueprints')
    site = models.ForeignKey(Site, on_delete=models.SET_DEFAULT, default="0")


class Picture(models.Model):
    file_name = models.CharField(max_length=100)
    file = models.FileField(upload_to='pictures')
    site = models.ForeignKey(Site, on_delete=models.SET_DEFAULT, default="0")


class Form(models.Model):
    file_name = models.CharField(max_length=100)
    file = models.FileField(upload_to='forms')
    location = models.CharField(max_length=200)
    date = models.DateField()
    separator = models.CharField(max_length=200)
    site = models.ForeignKey(Site, on_delete=models.SET_DEFAULT, default="0")


class Quote(models.Model):
    quote_completed = models.BooleanField(editable=False, default=False)
    building_completed = models.BooleanField(editable=False, default=False)

    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=16)
    country = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)

    # property info
    zoning = models.CharField(choices=EMPTY_SELECTION + ZONES, max_length=100)
    purpose = models.CharField(choices=EMPTY_SELECTION + PURPOSE, max_length=100)
    property = models.CharField(choices=EMPTY_SELECTION + PROPERTY, max_length=100)
    timeline = models.CharField(choices=EMPTY_SELECTION + TIMELINE, max_length=100)

    # basic building info
    width = models.IntegerField()
    length = models.IntegerField()
    height = models.IntegerField()

    # basic info choices
    style = models.CharField(choices=EMPTY_SELECTION + STYLE, max_length=100)
    colour = models.CharField(choices=EMPTY_SELECTION + COLOUR, max_length=100)
    install = models.CharField(choices=EMPTY_SELECTION + YES_NO, max_length=100)

    # insulation
    insul_roof = models.CharField(choices=EMPTY_SELECTION + INSULATION_ROOF, max_length=100)
    insul_walls = models.CharField(choices=EMPTY_SELECTION + INSULATION_WALL, max_length=100)

    # gutters
    gutters = models.CharField(choices=EMPTY_SELECTION + GUTTERS, max_length=100)

    # doors
    walk_doors = models.IntegerField()
    overhead_doors = models.IntegerField()
    oh_door_height = models.IntegerField()

    # door location
    oh_door_LE = models.BooleanField()
    oh_door_RE = models.BooleanField()
    oh_door_FS = models.BooleanField()
    oh_door_BS = models.BooleanField()

    # additional info
    additional = models.CharField(max_length=500, blank=True)


class Rectangle(models.Model):
    side_ab = models.CharField(max_length=10)
    side_ac = models.CharField(max_length=10)
    side_bd = models.CharField(max_length=10)
    side_cd = models.CharField(max_length=10)
    diag_ad = models.CharField(max_length=10)
    diag_bc = models.CharField(max_length=10)


