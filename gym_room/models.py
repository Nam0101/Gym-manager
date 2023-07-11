from django.db import models

# Create your models here.

class room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField('Name', max_length=50)
    room_location = models.CharField('Location', max_length=50)