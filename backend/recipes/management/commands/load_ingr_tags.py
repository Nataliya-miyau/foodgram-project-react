import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Tag


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'color': '#00ff7f', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#f754e1', 'slug': 'lunch'},
            {'name': 'Ужин', 'color': '#00bfff', 'slug': 'dinner'}]
        Tag.objects.bulk_create(Tag(**tag) for tag in data)

        with open(
                'recipes/data/ingredients.csv', 'r',
                encoding='UTF-8'
        ) as ingredients:
            reader = csv.reader(ingredients, delimiter=",")
            for row in reader:
                Ingredient.objects.get_or_create(
                    name=row[0], measurement_unit=row[1],
                )
        self.stdout.write(self.style.SUCCESS('Ингрeдиенты и теги загружены'))
