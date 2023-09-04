# Generated by Django 3.2 on 2023-03-12 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0052_auto_20230312_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresult',
            name='nitrogen_level',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='measured in ppm-parts per milliions', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='organic_matter',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='measured in t/ha tonne per hectare', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='phosphorus_level',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='measured in ppm-parts per millions', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='potassium_level',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='measured in ppm-parts per millions', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='soil_moisture',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='measured in water fraction by volute m3m-3', max_digits=10, null=True),
        ),
    ]