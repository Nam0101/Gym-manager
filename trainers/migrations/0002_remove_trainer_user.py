# Generated by Django 4.2.3 on 2023-07-17 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainer',
            name='user',
        ),
    ]
