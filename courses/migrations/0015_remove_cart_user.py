# Generated by Django 4.2.6 on 2023-12-03 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_rename_author_cart_user_remove_cart_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='user',
        ),
    ]
