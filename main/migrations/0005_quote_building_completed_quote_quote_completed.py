# Generated by Django 4.1.3 on 2022-12-14 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='building_completed',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='quote',
            name='quote_completed',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
