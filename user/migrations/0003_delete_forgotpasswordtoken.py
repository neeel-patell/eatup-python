# Generated by Django 3.1.6 on 2021-04-07 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_forgotpasswordtoken'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ForgotPasswordToken',
        ),
    ]
