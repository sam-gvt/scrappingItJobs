# Generated by Django 5.0.6 on 2024-06-25 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='experience',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='job',
            name='mission_duration',
            field=models.CharField(max_length=200),
        ),
    ]
