from django.db import models


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
    date = models.DateField()


class Equipment(models.Model):
    owned = models.BooleanField()
    type = models.CharField(max_length=200)
    unit_num = models.IntegerField()
    mileage = models.IntegerField()
    last_service = models.DateField()
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


