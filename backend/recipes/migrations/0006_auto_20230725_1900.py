# Generated by Django 3.2.16 on 2023-07-25 16:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0005_ingredient_unique_ingredient'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'default_related_name': 'favorite', 'verbose_name': 'Избранный рецепт', 'verbose_name_plural': 'Избранные рецепты'},
        ),
        migrations.AlterModelOptions(
            name='ingredientrecipe',
            options={'ordering': ['recipe'], 'verbose_name': 'Количество ингредиента', 'verbose_name_plural': 'Количество ингредиентов рецепта'},
        ),
        migrations.AlterModelOptions(
            name='shopping_cart',
            options={'default_related_name': 'shopping_cart', 'verbose_name': 'Список покупок'},
        ),
        migrations.AlterField(
            model_name='shopping_cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
