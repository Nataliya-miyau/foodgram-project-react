from django.contrib import admin
from django.contrib.admin import TabularInline

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            Shopping_cart, Tag)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name', 'measurement_unit',)
    list_filter = ('name',)
    empty_value_display = '- пусто -'


class IngredientRecipeInline(TabularInline):
    model = IngredientRecipe
    min_num = 1
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('name', 'color',)
    list_filter = ('name', 'color',)
    empty_value_display = '- пусто -'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'get_ingredients',
                    'get_tags', 'favorite')
    search_fields = ('name', 'author', 'tags')
    list_filter = ('name', 'author', 'tags')
    inlines = (IngredientRecipeInline,)
    empty_value_display = '- пусто -'

    def favorite(self, obj):
        return obj.favorite.count()

    favorite.short_description = 'Избранное'

    def get_ingredients(self, obj):
        ingredients_list = []
        for ingredient in obj.ingredients.all():
            ingredients_list.append(ingredient.name.lower())
        return ', '.join(ingredients_list)

    get_ingredients.short_description = 'Ингрeдиенты'

    def get_tags(self, obj):
        list_ = [_.name for _ in obj.tags.all()]
        return ', '.join(list_)


@admin.register(Shopping_cart)
class ShoppingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    search_fields = ('user', 'recipe', )
    empty_value_display = '- пусто -'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    search_fields = ('user', 'recipe', )
    empty_value_display = '- пусто -'
