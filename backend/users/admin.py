from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import Follow, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'id', 'email', 'first_name',
                    'last_name', 'quantity_recipes',
                    'quantity_followers')
    list_display_links = ('username', 'id')
    list_filter = ('email', 'username',)
    search_fields = ('username', 'email',)
    empty_value_display = '- пусто -'

    @admin.display(description='Количество рецептов')
    def quantity_recipes(self, obj):
        return obj.recipes.count()

    @admin.display(description='Количество подписчиков')
    def quantity_followers(self, obj):
        return obj.follower.count()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'author',)
    search_fields = ('user__email', 'author__email',)
    empty_value_display = '- пусто -'
