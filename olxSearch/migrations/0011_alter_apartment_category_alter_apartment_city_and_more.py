# Generated by Django 4.1.3 on 2022-12-04 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('olxSearch', '0010_rename_type_apartment_category_apartment_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='category',
            field=models.CharField(choices=[(0, 'mieszkania'), (1, 'Dziłki'), (2, 'Domy')], default=0, max_length=20),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RealEstateCities', to='olxSearch.city'),
        ),
        migrations.AlterField(
            model_name='searchingsettings',
            name='category',
            field=models.CharField(choices=[(0, 'mieszkania'), (1, 'Dziłki'), (2, 'Domy')], default=0, max_length=20),
        ),
    ]
