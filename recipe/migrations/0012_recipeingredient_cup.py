# Generated by Django 3.1.6 on 2021-03-25 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0011_auto_20210325_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeingredient',
            name='cup',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
