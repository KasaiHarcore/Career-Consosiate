# A separate urls file for the base app is created to manage the routing of the base app

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name = 'dashboard'),
    path('job/', views.job, name = 'job'),
    path('candidates/', views.candidate, name = 'candidates'),
    path('matching/', views.matching, name = 'matching'),
]