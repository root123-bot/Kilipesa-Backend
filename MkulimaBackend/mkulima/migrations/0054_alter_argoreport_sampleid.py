# Generated by Django 3.2 on 2023-03-12 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0053_auto_20230312_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='argoreport',
            name='sampleId',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
