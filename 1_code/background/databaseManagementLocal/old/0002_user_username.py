# Generated by Django 4.1 on 2023-05-04 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databaseManagementLocal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='UserName',
            field=models.CharField(default=1, help_text='UserName', max_length=30),
            preserve_default=False,
        ),
    ]
