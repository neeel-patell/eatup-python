# Generated by Django 3.1.6 on 2021-03-23 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_remove_recipeprecaution_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipesteps',
            name='sec_wait',
        ),
    ]