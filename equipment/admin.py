# Register your models here.
from django.contrib import admin

from .models import Equipment, Room

admin.site.register(Equipment)
admin.site.register(Room)