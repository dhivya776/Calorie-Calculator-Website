# Generated by Django 5.1.3 on 2024-12-03 05:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Fityfeed', '0018_alter_customer_calorie_limit_alter_customer_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='Fityfeed.customer')),
            ],
        ),
    ]
