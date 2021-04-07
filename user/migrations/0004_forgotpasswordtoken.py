# Generated by Django 3.1.6 on 2021-04-07 03:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_delete_forgotpasswordtoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForgotPasswordToken',
            fields=[
                ('token', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'forgot_password_token',
            },
        ),
    ]
