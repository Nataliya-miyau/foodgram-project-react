import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == "me":
        raise ValidationError(
            ('Нельзя использовать "me" в качестве username.'),
            params={"value": value},
        )
    if not re.match(r'^[a-zA-Z_.]*$', value):
        raise ValidationError('Имя может содержать только буквы')


def validate_name(value):
    if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s]*$', value):
        raise ValidationError('Имя может содержать только буквы')
