# Generated by Django 4.1 on 2023-05-10 12:41

import databaseManagementLocal.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databaseManagementLocal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='FoodPhoto',
            field=models.ImageField(blank=True, null=True, upload_to=databaseManagementLocal.models.Menu.user_directory_path),
        ),
    ]
