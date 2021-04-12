# Generated by Django 3.1.6 on 2021-04-12 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_homeuser_is_root'),
        ('recipe', '0015_reciperating_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipeschedule',
            name='user',
        ),
        migrations.AddField(
            model_name='recipeschedule',
            name='home',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, to='user.home'),
            preserve_default=False,
        ),
    ]
