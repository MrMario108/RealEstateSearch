# Generated by Django 4.1.3 on 2022-12-03 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olxSearch', '0008_alter_searchingsettings_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='slug',
            field=models.SlugField(default='', max_length=100),
        ),
    ]
