# Generated by Django 3.2 on 2023-03-04 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0032_auto_20230303_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='nextkin',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nextkin', to='mkulima.nextkeen'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='family',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='familydetails', to='mkulima.familydetails'),
        ),
    ]
