# Generated by Django 4.2.3 on 2023-07-08 06:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('members', '0036_alter_member_member_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='member_id',
            new_name='id',
        ),
    ]