from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Trainer(models.Model):
    trainer_id = models.AutoField(primary_key=True)
    trainer_name = models.CharField('Trainer Name', max_length=100)
    trainer_email = models.CharField('Trainer Email', max_length=100)
    trainer_phone = models.CharField('Trainer Phone', max_length=100)
    trainer_address = models.CharField('Trainer Address', max_length=100)
    dob = models.DateField(default='dd/mm/yyyy')
    start_work = models.DateField(auto_now_add=True)
    photo = models.FileField(upload_to='photos/', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
