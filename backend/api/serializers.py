from django.contrib.auth import get_user_model
from django.core.exceptions import BadRequest
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (CharField, IntegerField,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField, Serializer,
                                        SerializerMethodField)

from recipes.models import Favorite as FavoriteModel
from recipes.models import Ingredient as IngredientModel
from recipes.models import IngredientRecipe as IngredientRecipeModel
from recipes.models import Recipe as RecipeModel
from recipes.models import ShoppingСart as ShoppingСartModel
from recipes.models import Tag as TagModel
from recipes.validators import validate_name as validate_tagname
from users.validators import validate_name, validate_username

UserModel = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta:
        model = UserModel
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )

    def validate_name(self, value):
        validate_name(value)
        if len(value) > 254:
            raise ValidationError(
                "name should be shorter than 255 unicode codeunits"
            )

        return value

    def validate_username(self, value):
        validate_username(value)
        if len(value) > 150:
            raise ValidationError(
                "username should be shorter than 150 unicode codeunits"
            )

        return value

    def validate_first_name(self, value):
        if len(value) > 150:
            raise ValidationError(
                "Имя должно быть короче 150 символов."
            )

        return value

    def validate_last_name(self, value):
        if len(value) > 150:
            raise ValidationError(
                "Фамилия должна быть короче 150 символов."
            )

        return value

    def validate_password(self, value):
        if len(value) > 150:
            raise ValidationError(
                "Пароль должен быть короче 150 символов."
            )

        return value


class UserSerializer(BaseUserSerializer):

    class Meta:
        model = UserModel
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )


class UserWSubscriptionSerializer(UserSerializer):

    is_subscribed = SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            'is_subscribed',
        )

    def get_is_subscribed(self, instance):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False

        return instance.following.filter(user=request.user).exists()


class DummyUserSerializer(Serializer):

    pass


class TagSerializer(ModelSerializer):

    class Meta:
        model = TagModel
        fields = ("id", "name", "color", "slug")

    def validate_name(self, value):
        validate_tagname(value)
        return value


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = IngredientModel
        fields = ("id", "name", "measurement_unit")
        read_only_fields = fields


class IngredientInRecipeSerializer(ModelSerializer):

    id = IntegerField(source="ingredient.id")
    name = CharField(source="ingredient.name")
    measurement_unit = CharField(source="ingredient.measurement_unit")
    amount = IntegerField(min_value=1)

    class Meta:
        model = IngredientRecipeModel
        fields = (
            "id", "name", "measurement_unit", "amount",
        )
        read_only_fields = fields


class RecipeReadSerializer(ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = UserWSubscriptionSerializer(read_only=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    ingredients = IngredientInRecipeSerializer(
        source="ingredientrecipes", many=True
    )
    image = Base64ImageField(read_only=True)

    class Meta:
        model = RecipeModel
        fields = (
            "id", "tags", "author", "ingredients", "is_favorited",
            "is_in_shopping_cart", "name", "image", "text", "cooking_time",
        )

    def get_is_in_shopping_cart(self, instance):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False

        return ShoppingСartModel.objects.filter(
            user=request.user, recipe=instance
        ).exists()

    def get_is_favorited(self, instance):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False

        return FavoriteModel.objects.filter(
            user=request.user, recipe=instance
        ).exists()


class IngredientInRecipeWriteSerializer(Serializer):

    id = IntegerField()
    amount = IntegerField(min_value=1)

    class Meta:
        fields = ("id", "amount")

    def validate_id(self, id_value):
        if not IngredientModel.objects.filter(pk=id_value).exists():
            raise ValidationError("Specified ingredient does not exists")

        return id_value


class RecipeWriteSerializer(ModelSerializer):

    tags = PrimaryKeyRelatedField(queryset=TagModel.objects.all(), many=True)
    ingredients = IngredientInRecipeWriteSerializer(many=True)
    cooking_time = IntegerField(min_value=1)
    image = Base64ImageField()
    name = CharField(max_length=200)

    class Meta:
        model = RecipeModel
        fields = (
            "id", "ingredients", "tags",
            "image", "name", "text", "cooking_time",
        )

    def validate_ingredients(self, value):
        if not value:
            raise ValidationError("Должен быть хотя бы один ингредиент.")

        ids = list([x["id"] for x in value])
        if len(set(ids)) != len(ids):
            raise ValidationError("Ингредиенты должны быть уникальными.")

        return value

    def create(self, validated_data):

        request = self.context.get("request")
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")

        recipe = RecipeModel.objects.create(
            author=request.user,
            **validated_data
        )

        for ingr_def in ingredients:
            recipe.ingredientrecipes.create(
                ingredient_id=ingr_def["id"],
                recipe=recipe,
                amount=ingr_def["amount"]
            )

        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.tags.set(tags)
        instance.ingredientrecipes.all().delete()
        for ingr_def in ingredients:
            instance.ingredientrecipes.create(
                ingredient_id=ingr_def["id"],
                recipe=instance,
                amount=ingr_def["amount"]
            )

        instance.save()
        return instance


class RecipeSimpleSerializer(ModelSerializer):

    class Meta:
        model = RecipeModel
        fields = ("id", "name", "image", "cooking_time")


class UserWithRecipesSerializer(UserSerializer):

    recipes = SerializerMethodField(read_only=True)
    recipes_count = IntegerField(source='recipes.count', read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            "recipes",
            "recipes_count",
        )

    def get_recipes(self, instance):

        recipes_limit = self.context.get("recipes_limit", None)
        try:
            if recipes_limit is not None:
                recipes_limit = int(recipes_limit)
        except ValueError:
            raise BadRequest(
                "Недопустимый запрос. Должно быть число."
            )

        queryset = instance.recipes.order_by("-pub_date")
        rv = queryset.all()

        if recipes_limit is not None:
            rv = rv[:recipes_limit]

        serializer = RecipeSimpleSerializer(instance=rv, many=True)
        return serializer.data
