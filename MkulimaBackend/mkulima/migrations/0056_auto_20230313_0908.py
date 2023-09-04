# Generated by Django 3.2 on 2023-03-13 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0055_alter_argoreport_recommendation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresult',
            name='bulk_density',
            field=models.CharField(blank=True, help_text='Bulk density we measure in kg/m3', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='nitrogen_level',
            field=models.CharField(blank=True, help_text='measured in ppm-parts per milliions', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='organic_matter',
            field=models.CharField(blank=True, help_text='measured in t/ha tonne per hectare', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='phosphorus_level',
            field=models.CharField(blank=True, help_text='measured in ppm-parts per millions', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='potassium_level',
            field=models.CharField(blank=True, help_text='measured in ppm-parts per millions', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='soil_moisture',
            field=models.CharField(blank=True, help_text='measured in water fraction by volute m3m-3', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='soil_ph',
            field=models.CharField(blank=True, help_text='pH is decimal/number', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='soil_porosity',
            field=models.CharField(blank=True, help_text='Porosity is measured in g/cm**3', max_length=500, null=True),
        ),
    ]