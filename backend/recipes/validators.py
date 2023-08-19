import re

from django.core.exceptions import ValidationError


def validate_name(tagname):
    if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s]*$', tagname):
        raise ValidationError('Имя тега может содержать только буквы')
