# Generated by Django 3.2 on 2023-03-03 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0031_auto_20230303_1951'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nextkeen',
            name='family',
        ),
        migrations.AddField(
            model_name='nextkeen',
            name='national_ID',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
