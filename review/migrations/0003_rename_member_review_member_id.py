# Generated by Django 4.2.3 on 2023-07-08 06:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('review', '0002_remove_review_member_name_review_member'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='member',
            new_name='member_id',
        ),
    ]