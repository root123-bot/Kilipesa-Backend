# Generated by Django 3.2 on 2023-03-03 19:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0023_auto_20230303_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='gatheredinfo',
            name='assignedTo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignedto', to='mkulima.argonprofile'),
        ),
        migrations.AddField(
            model_name='gatheredinfo',
            name='assigned_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='gatheredinfo',
            name='isAssigned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='gatheredinfo',
            name='release_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]