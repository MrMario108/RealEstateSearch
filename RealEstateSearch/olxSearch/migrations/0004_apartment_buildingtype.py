# Generated by Django 4.1.6 on 2023-03-25 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('olxSearch', '0003_buildingtype_apartment_date_published2'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='buildingType',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='realEstateBuildingType', to='olxSearch.buildingtype'),
        ),
    ]
