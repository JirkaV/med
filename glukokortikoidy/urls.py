from django.conf.urls import *
from .import views

urlpatterns = [
    url(r'^$', views.calculator, name='glukokortikoidy_calculator'),
]
