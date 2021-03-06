# Generated by Django 3.1.6 on 2021-04-08 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20210407_0843'),
        ('recipe', '0013_recipeschedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='rating',
        ),
        migrations.AlterField(
            model_name='recipeschedule',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='RecipeRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=0, max_digits=1)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'recipe_rating',
            },
        ),
    ]
