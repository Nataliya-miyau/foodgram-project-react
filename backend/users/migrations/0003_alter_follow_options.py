# Generated by Django 3.2.16 on 2023-07-29 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230724_1542'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ['created'], 'verbose_name': 'Подписка', 'verbose_name_plural': 'Подписки'},
        ),
    ]
