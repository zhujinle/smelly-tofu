# Generated by Django 4.1 on 2023-05-06 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databaseManagementLocal', '0008_alter_user_license'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='CustomerDaily',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='CustomerSum',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
