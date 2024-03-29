# Generated by Django 4.1.3 on 2022-12-14 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_navmenuitem_dropdown'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(max_length=16)),
                ('country', models.CharField(max_length=50)),
                ('province', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('county', models.CharField(max_length=50)),
                ('postal_code', models.CharField(max_length=50)),
                ('zoning', models.CharField(choices=[('', '--Please Select--'), ('commercial', 'Commercial'), ('residential', 'Residential'), ('agricultural', 'Agricultural'), ('industrial', 'Industrial'), ('other', 'Other')], max_length=100)),
                ('purpose', models.CharField(choices=[('', '--Please Select--'), ('garage', 'Garage'), ('home', 'Home'), ('shed', 'Shed'), ('workshop', 'Workshop'), ('warehouse', 'Warehouse/Storage'), ('repair', 'Repair/Mechanic Shop'), ('agriculture', 'Agriculture'), ('retail', 'Retail Store'), ('factory', 'Factory/Assembly'), ('office', 'Office Space'), ('aviation', 'Aviation'), ('other', 'Other')], max_length=100)),
                ('property', models.CharField(choices=[('', '--Please Select--'), ('own', 'We own the property'), ('identified_financed', 'Identified property and arranged financing'), ('identified', 'Identified property, not financed'), ('no', 'No')], max_length=100)),
                ('timeline', models.CharField(choices=[('', '--Please Select--'), ('asap', 'ASAP'), ('1_3_months', '1-3 Months'), ('3_6_months', '3-6 Months'), ('6_12_months', '6-12 Months'), ('year', 'Over 1 year')], max_length=100)),
                ('width', models.IntegerField()),
                ('length', models.IntegerField()),
                ('height', models.IntegerField()),
                ('style', models.CharField(choices=[('', '--Please Select--'), ('gable', 'Straight wall style (gable)'), ('monoslope', 'Straight wall style (single slope)'), ('quonset', 'Arch style (Quonset)')], max_length=100)),
                ('colour', models.CharField(choices=[('', '--Please Select--'), ('standard', 'All Standard Colour Building'), ('galv_roof', 'Galvalume Roof, Standard Colour Walls'), ('all_galv', 'All Galvalume Building')], max_length=100)),
                ('install', models.CharField(choices=[('', '--Please Select--'), ('yes', 'Yes'), ('no', 'No')], max_length=100)),
                ('insul_roof', models.CharField(choices=[('', '--Please Select--'), ('2_inch', 'Yes - 2" thick'), ('4_inch', 'Yes - 4" thick'), ('6_inch', 'Yes - 6" thick'), ('no', 'No')], max_length=100)),
                ('insul_walls', models.CharField(choices=[('', '--Please Select--'), ('2_inch', 'Yes - 2" thick'), ('4_inch', 'Yes - 4" thick'), ('no', 'No')], max_length=100)),
                ('gutters', models.CharField(choices=[('', '--Please Select--'), ('both', 'Yes, Both Sidewalls'), ('fs', 'Yes, Front Sidewall Only'), ('bs', 'Yes, Back Sidewall Only'), ('no', 'No')], max_length=100)),
                ('walk_doors', models.IntegerField()),
                ('overhead_doors', models.IntegerField()),
                ('oh_door_height', models.IntegerField()),
                ('oh_door_LE', models.BooleanField()),
                ('oh_door_RE', models.BooleanField()),
                ('oh_door_FS', models.BooleanField()),
                ('oh_door_BS', models.BooleanField()),
                ('additional', models.CharField(blank=True, max_length=500)),
            ],
        ),
    ]
