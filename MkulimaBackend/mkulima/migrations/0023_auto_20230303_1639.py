# Generated by Django 3.2 on 2023-03-03 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0022_auto_20230303_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gatheredinfo',
            name='added_on',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='gatheredinfo',
            name='locked_at',
            field=models.DateTimeField(),
        ),
    ]