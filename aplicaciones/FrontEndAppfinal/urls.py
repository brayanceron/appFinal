from django.contrib import admin
from .views import *
from django.urls import path,include
urlpatterns = [
    path('home/', home),
    path('getCatalogoTutorias/',home),
    path('getTutoria/',getTutoria),
    
]