# Generated by Django 4.1 on 2023-05-05 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databaseManagementLocal', '0005_alter_menu_foodphoto_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='DeliveryStaffUID',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
