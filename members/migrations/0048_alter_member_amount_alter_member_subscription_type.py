# Generated by Django 4.2.3 on 2023-07-19 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0047_subscription_price_per_year_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='amount',
            field=models.CharField(blank=True, default='0', max_length=30),
        ),
        migrations.AlterField(
            model_name='member',
            name='subscription_type',
            field=models.CharField(choices=[('Gym', 'Gym'), ('Cross Fit', 'Cross Fit'), ('Gym + Cross Fit', 'Gym + Cross Fit'), ('Personal Training', 'Personal Training'), ('Cross Fit + Gym + Personal Training', 'Cross Fit + Gym + Personal Training')], default='gym', max_length=100, verbose_name='Subscription Type'),
        ),
    ]
