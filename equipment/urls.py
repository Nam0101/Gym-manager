from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required
from .models import *

urlpatterns = [
    path('add/', login_required(views.add_equipment), name='add_equipment'),
    path('view/', login_required(views.view_equipment), name='view_equipment'),
    path('search_equipment/', views.search_equipment, name='search_equipment'),
    path('update/<int:equipment_id>/', views.update_equipment, name='update_equipment'),
    path('add_equipment/', views.add_equipment, name='add_equipment'),
]
