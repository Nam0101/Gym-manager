# Generated by Django 4.2.3 on 2023-07-08 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0037_rename_member_id_member_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='id',
            new_name='member_id',
        ),
    ]
