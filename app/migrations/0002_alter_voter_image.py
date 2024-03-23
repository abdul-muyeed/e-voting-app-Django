# Generated by Django 5.0.3 on 2024-03-23 10:12

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='image',
            field=cloudinary.models.CloudinaryField(default='avatar.png', max_length=255, verbose_name='image'),
        ),
    ]
