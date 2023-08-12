from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from foodgram.settings import MAX_LENGHT_2
from users.validators import validate_name

User = get_user_model()


class Tag(models.Model):

    name = models.CharField(
        verbose_name='Название тега',
        max_length=MAX_LENGHT_2,
        unique=True,
        validators=(validate_name, )
    )
    color = ColorField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
        default='#FF0000',
    )
    slug = models.SlugField(
        verbose_name='Уникальный слаг',
        max_length=MAX_LENGHT_2,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):

    name = models.CharField(
        verbose_name='Наименование ингредиента',
        max_length=MAX_LENGHT_2,
        validators=(validate_name, )
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=MAX_LENGHT_2,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}.'


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True,
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=MAX_LENGHT_2,
        validators=(validate_name, )
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиент',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes',
    )
    image = models.ImageField(
        verbose_name='Фотография блюда',
        upload_to='recipes/image/',
        blank=True,
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        max_length=500,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(600)],
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class TagRecipe(models.Model):

    tag = models.ForeignKey(
        Tag,
        verbose_name='Теги',
        on_delete=models.CASCADE,
        related_name='tag_recipes',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='tag_recipes',
    )

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецептов'
        ordering = (
            'recipe__name',
            'tag__name',
        )
        unique_together = ('tag', 'recipe',)

    def __str__(self):
        return f"{self.id}: {self.recipe.name}, {self.tag.name}"


class IngredientRecipe(models.Model):

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=1,
        validators=(
            MinValueValidator(
                1, 'Количество должно быть не менее 1',
            ),
        ),
    )

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe_to_ingredient_exists')]

    def __str__(self):
        return (f'{self.recipe}: {self.ingredient.name},'
                f' {self.amount}')


class FavoriteShoppingCartModel(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class Favorite(FavoriteShoppingCartModel):

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        default_related_name = 'favorite'
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='favorite_unique_recipe'
            )
        ]


class Shopping_сart(FavoriteShoppingCartModel):

    class Meta:
        verbose_name = 'Список покупок'
        default_related_name = 'shopping_cart'
        constraints = [
            UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_recipe_in_shopping_cart'
            )
        ]
