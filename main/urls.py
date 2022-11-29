from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("about-us", views.about_us, name='about us'),
    path("aircraft-hangars", views.aircraft_hangars, name='aircraft hangars'),
    path("commercial-industrial", views.commercial_industrial, name='commercial industrial'),
    path("farm-ranch", views.farm_ranch, name='farm ranch'),
    path("heritage-buildings", views.heritage_buildings, name='heritage buildings'),
    path("storage-units", views.storage_units, name='storage units'),
    path("workshops", views.workshops, name='workshops'),
    path("clear-span", views.clear_span, name='clear span'),
    path("multi-span", views.multi_span, name='multi span'),
    path("cladding", views.cladding, name='cladding'),
    path("structural-sections", views.structural_sections, name='structural sections'),
    path("doors", views.doors, name='doors'),
    path("erection", views.erection, name='erection'),
    path("glossary", views.glossary, name='glossary'),
    path("photos", views.photos, name='photos'),
    path("contact", views.contact, name='contact us'),
]
