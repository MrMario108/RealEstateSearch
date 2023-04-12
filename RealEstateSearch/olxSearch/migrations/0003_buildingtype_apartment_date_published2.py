# Generated by Django 4.1.6 on 2023-03-25 08:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('olxSearch', '0002_htmltagsnametofind'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='apartment',
            name='date_published2',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
