# Generated by Django 3.1.6 on 2021-04-24 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='schdule',
            new_name='schedule',
        ),
    ]
