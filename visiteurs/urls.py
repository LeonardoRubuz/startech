# Raikage The Third

from django.urls import path

from .views import *

urlpatterns =[
    path('', homepage, name='home'),
    path('demande-de-devis/', DevisPageView.as_view(), name='devis'),
    path('marketing/', marketing, name='marketing'),
    path('mobile-app/', mobile, name='mobileapp'),
    path('software-development/', softwares, name='softwaredev'),
    path('website-development/', website, name='websitedev'),

]