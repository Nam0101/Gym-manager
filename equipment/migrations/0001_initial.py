# Generated by Django 3.1.2 on 2023-07-03 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment_name', models.CharField(max_length=50, verbose_name='Name')),
                ('equipment_code', models.CharField(max_length=50, unique=True, verbose_name='Code')),
                ('equipment_quantity', models.IntegerField(verbose_name='Quantity')),
                ('equipment_import_date', models.DateField(verbose_name='Import Date')),
                ('equipment_warranty_date', models.DateField(verbose_name='Warranty Date')),
                ('equipment_origin', models.CharField(max_length=50, verbose_name='Origin')),
                ('equipment_status', models.CharField(max_length=50, verbose_name='Status')),
            ],
        ),
    ]
