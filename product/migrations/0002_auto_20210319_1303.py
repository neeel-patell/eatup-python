# Generated by Django 3.1.6 on 2021-03-19 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productcategory',
            name='image',
        ),
        migrations.DeleteModel(
            name='ProductCategoryImage',
        ),
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]
