# Generated by Django 3.2 on 2023-05-17 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0075_auto_20230504_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='nationalID',
            field=models.CharField(blank=True, max_length=8000, null=True),
        ),
    ]
