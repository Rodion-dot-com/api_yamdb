# Generated by Django 2.2.16 on 2022-11-04 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0017_auto_20221102_0124'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('-id',), 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-id',), 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('-id',), 'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('-id',), 'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('-id',), 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Описание'),
            preserve_default=False,
        ),
    ]
