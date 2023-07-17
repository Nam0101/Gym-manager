# Generated by Django 4.2.3 on 2023-07-17 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainers', '0001_initial'),
        ('members', '0041_member_room_manager'),
    ]

    operations = [
        migrations.CreateModel(
            name='Training_history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_date', models.DateField(auto_now_add=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.member')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainers.trainer')),
            ],
        ),
    ]
