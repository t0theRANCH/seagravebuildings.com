# Generated by Django 4.1.3 on 2022-12-17 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_user_verifyaccount'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
