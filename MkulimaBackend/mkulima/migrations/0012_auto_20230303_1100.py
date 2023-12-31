# Generated by Django 3.2 on 2023-03-03 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0011_auto_20230303_0720'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoilMetadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('BLACK', 'BLACK'), ('RED', 'RED'), ('WHITE', 'WHITE'), ('BROWN', 'BROWN'), ('GREY', 'GREY'), ('YELLOW', 'YELLOW')], max_length=500)),
                ('temperature', models.IntegerField(help_text='Temperature is measured in Centigrades')),
                ('structure', models.CharField(choices=[('PLATY', 'PLATY'), ('PLISMATIC', 'PLISMATIC'), ('COLUMNAR', 'COLUMNAR'), ('GRANULAR', 'GRANULAR'), ('BLOCKY', 'BLOCKY')], max_length=500)),
                ('texture', models.CharField(choices=[('SAND', 'SAND'), ('LOAMY SAND', 'LOAMY SAND'), ('SANDY LOAM', 'SANDY LOAM'), ('LOAM', 'LOAM')], max_length=500)),
                ('porosity', models.DecimalField(decimal_places=2, help_text='Porosity is measured in g/cm**3', max_digits=3)),
                ('ph', models.DecimalField(decimal_places=1, help_text='pH is decimal/number', max_digits=3)),
                ('form', models.CharField(choices=[('SAND', 'SAND'), ('SILT', 'SILT'), ('CLAY', 'CLAY')], max_length=200)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='farm',
            name='farm_metadata',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='gatheredinfo', to='mkulima.gatheredinfo'),
        ),
        migrations.AddField(
            model_name='farm',
            name='soil',
            field=models.OneToOneField(default='1234', on_delete=django.db.models.deletion.CASCADE, related_name='smetadata', to='mkulima.soilmetadata'),
        ),
    ]
