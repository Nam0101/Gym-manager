# Generated by Django 4.2.3 on 2023-07-08 06:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('members', '0034_member_trainer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='member_id',
            field=models.AutoField(default=None, primary_key=True, serialize=False),
        ),
    ]
