# Generated by Django 4.1 on 2023-05-04 11:18

import databaseManagementLocal.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databaseManagementLocal', '0002_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Avatar',
            field=models.ImageField(blank=True, height_field=300, upload_to=databaseManagementLocal.models.User.user_directory_path, width_field=300),
        ),
        migrations.AlterField(
            model_name='user',
            name='Cart',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='License',
            field=models.ImageField(blank=True, upload_to=databaseManagementLocal.models.User.user_directory_path),
        ),
    ]
