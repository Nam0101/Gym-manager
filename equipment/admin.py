# Register your models here.
from django.contrib import admin

from .models import Equipment, room

admin.site.register(Equipment)
admin.site.register(room)