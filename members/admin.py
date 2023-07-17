from django.contrib import admin

from trainers.models import Trainer
# Register your models here.
from .models import Member, Manager

admin.site.register(Member)
admin.site.register(Manager)
admin.site.site_header = 'Gym Management System'
admin.site.site_title = 'Gym Management System'
admin.site.register(Trainer)