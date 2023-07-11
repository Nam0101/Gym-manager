# Generated by Django 4.2.3 on 2023-07-11 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='room',
            fields=[
                ('room_id', models.AutoField(primary_key=True, serialize=False)),
                ('room_name', models.CharField(max_length=50, verbose_name='Name')),
                ('room_location', models.CharField(max_length=50, verbose_name='Location')),
            ],
        ),
    ]