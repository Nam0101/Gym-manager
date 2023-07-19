# Generated by Django 4.2.3 on 2023-07-19 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0050_alter_training_history_training_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='batch',
            field=models.CharField(choices=[('morning', 'Morning'), ('evening', 'Evening'), ('both', 'All Day')], default='morning', max_length=30),
        ),
    ]