# Generated by Django 4.2.3 on 2023-07-08 06:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('members', '0035_alter_member_member_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='member_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
