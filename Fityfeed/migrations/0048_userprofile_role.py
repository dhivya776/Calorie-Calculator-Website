# Generated by Django 5.1.3 on 2024-12-06 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Fityfeed', '0047_alter_exercise_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('admin', 'Admin')], default='user', max_length=20),
        ),
    ]
