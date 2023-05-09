# Generated by Django 4.1 on 2023-05-05 08:30

import databaseManagementLocal.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databaseManagementLocal', '0004_user_newsessiontoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='FoodPhoto',
            field=models.ImageField(upload_to=databaseManagementLocal.models.Menu.user_directory_path),
        ),
        migrations.AlterField(
            model_name='user',
            name='Avatar',
            field=models.ImageField(blank=True, upload_to=databaseManagementLocal.models.User.user_directory_path),
        ),
    ]
