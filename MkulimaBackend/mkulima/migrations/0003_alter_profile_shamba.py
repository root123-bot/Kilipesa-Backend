# Generated by Django 3.2 on 2023-02-27 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0002_alter_profile_shamba'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='shamba',
            field=models.ManyToManyField(blank=True, to='mkulima.Shamba'),
        ),
    ]
