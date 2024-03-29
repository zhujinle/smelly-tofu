# Generated by Django 4.1 on 2023-05-06 01:06

import databaseManagementLocal.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databaseManagementLocal', '0006_alter_order_deliverystaffuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='NewSessionToken',
        ),
        migrations.AlterField(
            model_name='user',
            name='License',
            field=models.ImageField(upload_to=databaseManagementLocal.models.User.user_directory_path),
        ),
        migrations.AlterField(
            model_name='user',
            name='UserName',
            field=models.CharField(max_length=20),
        ),
    ]
