# Generated by Django 2.2.24 on 2021-06-13 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0014_usergroups'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserGroups',
        ),
    ]