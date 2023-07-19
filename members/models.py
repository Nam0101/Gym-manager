from django import forms
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.forms import ModelForm
from equipment.models import Room
from equipment.models import DEFAULT_ROOM_ID
from trainers.models import Trainer

SUBSCRIPTION_TYPE_CHOICES = (
    ('gym', 'Gym'),
    ('cross_fit', 'Cross Fit'),
    ('gym_and_cross_fit', 'Gym + Cross Fit'),
    ('pt', 'Personal Training')
)

SUBSCRIPTION_PERIOD_CHOICES = (
    ('1', '1 Month'),
    ('2', '2 Months'),
    ('3', '3 Months'),
    ('4', '4 Months'),
    ('5', '5 Months'),
    ('6', '6 Months'),
    ('7', '7 Months'),
    ('8', '8 Months'),
    ('9', '9 Months'),
    ('10', '10 Months'),
    ('11', '11 Months'),
    ('12', '12 Months'),
    ('24', '24 Months'),
)

FEE_STATUS = (
    ('paid', 'Paid'),
    ('pending', 'Pending'),
)

STATUS = (
    (0, 'Start'),
    (1, 'Stop'),
)

BATCH = (
    ('morning', 'Morning'),
    ('evening', 'Evening'),
    ('both', 'All Day'),
)


class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    subscription_type = models.CharField('Subscription Type', max_length=50)
    status = models.IntegerField(choices=STATUS, default=0)
    price_per_month = models.IntegerField('Price Per Month', default=0)
    price_per_year = models.IntegerField('Price Per Year', default=0)

    def __str__(self):
        return self.subscription_type


class Manager(models.Model):
    manager_id = models.AutoField(primary_key=True)
    manager_name = models.CharField('Manager Name', max_length=100)
    manager_email = models.CharField('Manager Email', max_length=100)
    manager_phone = models.CharField('Manager Phone', max_length=100)
    manager_address = models.CharField('Manager Address', max_length=100)
    dob = models.DateField(default='dd/mm/yyyy')
    start_work = models.DateField(auto_now_add=True)
    photo = models.FileField(upload_to='photos/', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey('equipment.Room', on_delete=models.CASCADE, default=DEFAULT_ROOM_ID)

    def __str__(self):
        return self.manager_name


class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    first_name = models.CharField('First Name', max_length=50)
    last_name = models.CharField('Last Name', max_length=50)
    mobile_number = models.CharField('Mobile Number', max_length=10, unique=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=300, blank=True)
    medical_history = models.CharField('Medical History', max_length=300, blank=True, default='None')
    admitted_on = models.DateField(auto_now_add=True)
    registration_date = models.DateField('Registration Date', default='dd/mm/yyyy')
    registration_upto = models.DateField()
    dob = models.DateField(default='dd/mm/yyyy')
    subscription_type = models.CharField(
        'Subscription Type',
        max_length=100,
        choices=Subscription.objects.filter(status=0).values_list('subscription_type', 'subscription_type'),
        default=SUBSCRIPTION_TYPE_CHOICES[0][0]
    )
    subscription_period = models.CharField(
        'Subscription Period',
        max_length=30,
        choices=SUBSCRIPTION_PERIOD_CHOICES,
        default=SUBSCRIPTION_PERIOD_CHOICES[0][0]
    )
    amount = models.CharField(max_length=30, blank=True, default='0')
    fee_status = models.CharField(
        'Fee Status',
        max_length=30,
        choices=FEE_STATUS,
        default=FEE_STATUS[0][0]
    )
    batch = models.CharField(
        max_length=30,
        choices=BATCH,
        default=BATCH[0][0]
    )
    photo = models.FileField(upload_to='photos/', blank=True)
    notification = models.IntegerField(default=2, blank=True)
    stop = models.IntegerField('Status', choices=STATUS, default=STATUS[0][0], blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey('equipment.Room', on_delete=models.CASCADE, blank=True, default=DEFAULT_ROOM_ID)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Training_history(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, blank=True, null=True)
    training_date = models.DateField(default='dd/mm/yyyy')

    def __str__(self):
        return self.member.first_name + ' ' + self.member.last_name + ' - ' + self.trainer.trainer_name
