# Generated by Django 5.0.6 on 2024-06-25 01:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_job_title_alert_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('tjm', models.IntegerField()),
                ('localization', models.CharField(max_length=200)),
                ('experience', models.IntegerField()),
                ('esn', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('mission_duration', models.IntegerField()),
                ('id_alert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.alert')),
            ],
        ),
    ]