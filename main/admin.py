from django.contrib import admin
from .models import Site, Equipment, Blueprint, Picture, Form, Quote, NewUser, VerifyAccount

admin.site.register(Site)
admin.site.register(Equipment)
admin.site.register(Blueprint)
admin.site.register(Picture)
admin.site.register(Form)
admin.site.register(Quote)
admin.site.register(NewUser)
admin.site.register(VerifyAccount)
