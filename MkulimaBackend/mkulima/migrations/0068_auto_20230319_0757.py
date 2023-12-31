# Generated by Django 3.2 on 2023-03-19 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0067_auto_20230317_2053'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop', models.CharField(blank=True, max_length=200, null=True)),
                ('season', models.CharField(blank=True, max_length=200, null=True)),
                ('fertilizers', models.CharField(blank=True, max_length=800, null=True)),
                ('seed_amonunt_per_size_of_farm_or_hectare', models.CharField(blank=True, max_length=800, null=True)),
                ('cultivation_type', models.CharField(blank=True, max_length=800, null=True)),
                ('standard_yield', models.CharField(blank=True, help_text='Unaweza ukapata magunia mangapi ukifata ushauri wake tunatumia magunia haya makubwa ya kilo 120', max_length=900, null=True)),
                ('brief_explanation', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='argoreport',
            name='recommendation',
        ),
    ]
