from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
urlpatterns = [
    path('add/', login_required(views.add_review), name='add_review'),
    path('view/', login_required(views.view_reviews), name='view_review'),
    path('my_reviews/', login_required(views.my_reviews), name='my_reviews'),
]
