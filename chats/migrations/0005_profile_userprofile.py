# Generated by Django 3.2.4 on 2021-06-07 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0004_auto_20210607_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='userprofile',
            field=models.CharField(default='', max_length=100),
        ),
    ]