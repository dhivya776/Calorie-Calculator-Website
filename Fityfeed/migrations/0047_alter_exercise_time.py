# Generated by Django 5.1.3 on 2024-12-05 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Fityfeed', '0046_alter_exercise_time'),
    ]

    operations = [
        migrations.RunSQL(
            sql='ALTER TABLE "Fityfeed_exercise" ALTER COLUMN "time" TYPE time USING to_timestamp("time")::time;',
            reverse_sql='ALTER TABLE "exercise" ALTER COLUMN "time" TYPE integer;',

        ),
        migrations.AlterField(
            model_name='exercise',
            name='time',
            field=models.TimeField(),
        ),
        
    ]