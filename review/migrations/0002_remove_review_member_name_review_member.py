# Generated by Django 4.2.3 on 2023-07-08 06:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('members', '0034_member_trainer'),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='member_name',
        ),
        migrations.AddField(
            model_name='review',
            name='member',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='members.member'),
            preserve_default=False,
        ),
    ]
