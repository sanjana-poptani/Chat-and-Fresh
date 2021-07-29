# Generated by Django 2.0 on 2021-07-18 18:40

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0080_auto_20210718_1742'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrpMsges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(default='', max_length=1200)),
                ('file', models.FileField(default='', upload_to='file/')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chats.groupModel')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chats.Profile')),
            ],
        ),
        migrations.RemoveField(
            model_name='usergroups',
            name='file',
        ),
        migrations.RemoveField(
            model_name='usergroups',
            name='message',
        ),
        migrations.RemoveField(
            model_name='usergroups',
            name='timestamp',
        ),
    ]