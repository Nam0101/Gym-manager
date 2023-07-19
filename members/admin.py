from django.contrib import admin

# Register your models here.
from .models import Member, Manager, Subscription

admin.site.register(Member)
admin.site.register(Manager)
admin.site.site_header = 'Gym Management System'
admin.site.site_title = 'Gym Management System'
admin.site.register(Subscription)