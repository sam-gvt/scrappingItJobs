# Generated by Django 5.0.6 on 2024-06-24 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alert',
            old_name='job_title',
            new_name='title',
        ),
    ]
