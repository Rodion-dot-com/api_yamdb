# Generated by Django 2.2.16 on 2022-10-27 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0012_auto_20221027_1621'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-id']},
        ),
    ]
