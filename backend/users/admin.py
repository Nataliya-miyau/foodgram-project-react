from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import Follow, User

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',)
    list_filter = ('email', 'username',)
    search_fields = ('username', 'email',)
    empty_value_display = '- пусто -'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author',)
    search_fields = ('user__email', 'author__email',)
    empty_value_display = '- пусто -'
