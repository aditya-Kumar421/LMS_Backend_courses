# Generated by Django 4.2.6 on 2023-12-03 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_cart_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='image_url',
            field=models.ImageField(upload_to='course_cart_images/'),
        ),
    ]
