# Generated by Django 4.2.6 on 2023-11-30 16:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_course_image_url_sector_sector_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='image_url',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='course_images/'),
            preserve_default=False,
        ),
    ]