# Generated by Django 3.2 on 2023-03-04 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0033_auto_20230304_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='gatheredinfo',
            name='coordinates',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='farm_coordinates', to='mkulima.size'),
        ),
    ]
