# Generated by Django 4.2.3 on 2023-07-04 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='business_revenue',
            fields=[
                ('revenue_id', models.AutoField(primary_key=True, serialize=False)),
                ('revenue_name', models.CharField(max_length=50)),
                ('revenue_month', models.CharField(max_length=50)),
                ('revenue_total', models.IntegerField()),
                ('revenue_type', models.CharField(max_length=50)),
                ('revenue_status', models.CharField(max_length=50)),
            ],
        ),
    ]
