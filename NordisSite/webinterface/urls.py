from django.urls import path, include
from . import views

app_name = 'webinterface'

urlpatterns = [
    path('', views.main, name="hom"),
    path('contact', views.contact, name="contact"),
]
