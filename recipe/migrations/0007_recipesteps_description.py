# Generated by Django 3.1.6 on 2021-03-23 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_remove_recipesteps_sec_wait'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipesteps',
            name='description',
            field=models.TextField(),
            preserve_default=False,
        ),
    ]
