from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("", views.MainView.as_view(template_name='main/home.html'), name='home'),
    path("login", views.sign_in, name='login'),
    path("logout", views.sign_out, name='logout'),
    path("sign-up", views.sign_up, name='sign-up'),
    path("confirmation-sent", views.confirmation_sent, name='confirmation-sent'),
    path('activate/<uid>/<token>', views.activate, name='activate'),
    path('activate-account', view=TemplateView.as_view(template_name='registration/activate_account.html'), name='activated'),
    path('password-change/<uid>/<token>', views.change_password, name='change-password'),
    path('password-change-complete', view=TemplateView.as_view(template_name='registration/change_password_complete.html'), name='change-password-complete'),
    path("forgot-password", views.password_reset, name='password-reset'),
    path("forgot-password-sent", views.ConfirmationView.as_view(template_name='registration/forgot_password_sent.html', info={'email': ''}), name='password-reset-sent'),
    path("quote.html", views.QuoteView.as_view(template_name='main/quote.html'), name='quote'),
    path("request-quote", views.ConfirmationView.as_view(template_name='main/request_quote.html', info={'name': '', 'phone': 'your phone number'}), name='request-quote'),
    path("about_us.html", views.MainView.as_view(template_name='main/about_us.html'), name='about us'),
    path("aircraft_hangars.html", views.MainView.as_view(template_name='main/aircraft_hangars.html'), name='aircraft hangars'),
    path("commercial_industrial.html", views.MainView.as_view(template_name='main/commercial_industrial.html'), name='commercial industrial'),
    path("farm_ranch.html", views.MainView.as_view(template_name='main/farm_ranch.html'), name='farm ranch'),
    path("heritage_buildings.html", views.MainView.as_view(template_name='main/heritage_buildings.html'), name='heritage buildings'),
    path("storage_units.html", views.MainView.as_view(template_name='main/storage_units.html'), name='storage units'),
    path("workshops.html", views.MainView.as_view(template_name='main/workshops.html'), name='workshops'),
    path("clear_span_structures.html", views.MainView.as_view(template_name='main/clear_span_structures.html'), name='clear span'),
    path("multi_span_structures.html", views.MainView.as_view(template_name='main/multi_span_structures.html'), name='multi span'),
    path("cladding.html", views.MainView.as_view(template_name='main/cladding.html'), name='cladding'),
    path("structural_sections.html", views.MainView.as_view(template_name='main/structural_sections.html'), name='structural sections'),
    path("doors.html", views.MainView.as_view(template_name='main/doors.html'), name='doors'),
    path("erection.html", views.MainView.as_view(template_name='main/erection.html'), name='erection'),
    path("glossary.html", views.MainView.as_view(template_name='main/glossary.html'), name='glossary'),
    path("photos.html", views.MainView.as_view(template_name='main/photos.html'), name='photos'),
    path("contact.html", views.MainView.as_view(template_name='main/contact.html'), name='contact us'),
    path('layout-calculator', views.layout_calculator, name='layout-calculator')
]
