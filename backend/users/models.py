from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from foodgram.settings import MAX_EMAIL_LENGHT, MAX_LENGHT_1
from users.validators import validate_name, validate_username


class User(AbstractUser):

    email = models.EmailField(
        verbose_name='Почта',
        max_length=MAX_EMAIL_LENGHT,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Логин',
        max_length=MAX_LENGHT_1,
        unique=True,
        validators=(validate_username, UnicodeUsernameValidator, ),
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=MAX_LENGHT_1,
        blank=False,
        validators=(validate_name, ),
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=MAX_LENGHT_1,
        blank=False,
        validators=(validate_name, ),
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=MAX_LENGHT_1,
    )

    class Meta:
        ordering = ('username', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}, {self.email}'


class Follow(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    created = models.DateTimeField(
        verbose_name='Дата подписки',
        auto_now_add=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follower')
        ]

    def __str__(self):
        return f'{self.user} - {self.author}'
