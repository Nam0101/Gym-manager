from django.contrib import admin
# Register your models here.
from .models import Member, Manager

admin.site.register(Member)
admin.site.register(Manager)
