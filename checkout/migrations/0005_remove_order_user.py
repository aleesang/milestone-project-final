# Generated by Django 3.1 on 2020-08-21 03:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_merge_20200821_0304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
    ]
