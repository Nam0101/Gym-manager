# Generated by Django 4.2.3 on 2023-07-18 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0043_subscription_alter_member_subscription_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='id',
        ),
        migrations.AddField(
            model_name='subscription',
            name='price_per_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='status',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='subscription',
            name='subscription_type_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='price_per_month',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
