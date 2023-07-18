from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('view/', login_required(views.view_training_history), name='view_training_history'),
]