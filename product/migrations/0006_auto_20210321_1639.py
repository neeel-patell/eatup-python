# Generated by Django 3.1.6 on 2021-03-21 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20210321_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productquantity',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
    ]
