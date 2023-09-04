# Generated by Django 3.2 on 2023-03-12 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0051_argoreport_is_completed_and_recommended'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresult',
            name='bulk_density',
            field=models.DecimalField(blank=True, decimal_places=5, help_text='Bulk density we measure in kg/m3', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='nitrogen_level',
            field=models.IntegerField(blank=True, help_text='measured in ppm-parts per milliions', null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='organic_matter',
            field=models.IntegerField(blank=True, help_text='measured in t/ha tonne per hectare', null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='phosphorus_level',
            field=models.IntegerField(blank=True, help_text='measured in ppm-parts per millions', null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='potassium_level',
            field=models.IntegerField(blank=True, help_text='measured in ppm-parts per millions', null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='sample_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='soil_color',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='soil_form',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='soil_moisture',
            field=models.IntegerField(blank=True, help_text='measured in water fraction by volute m3m-3', null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='soil_ph',
            field=models.DecimalField(blank=True, decimal_places=1, help_text='pH is decimal/number', max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='soil_porosity',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Porosity is measured in g/cm**3', max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='soil_structure',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='soil_temperature',
            field=models.IntegerField(blank=True, help_text='Temperature is measured in Centigrades', null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='soil_texture',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
