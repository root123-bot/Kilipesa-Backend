# Generated by Django 3.2 on 2023-03-03 16:37

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0019_alter_argoreport_added_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='gatheredinfo',
            name='added_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 3, 16, 37, 14, 975697)),
        ),
        migrations.AddField(
            model_name='gatheredinfo',
            name='is_locked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='gatheredinfo',
            name='locked_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 3, 16, 37, 14, 975720)),
        ),
        migrations.AddField(
            model_name='gatheredinfo',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='gatheredinfo',
            name='gathered_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gathered_by', to='mkulima.gatherprofile'),
        ),
        migrations.AlterField(
            model_name='gatheredinfo',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='farm_owner', to='mkulima.owner'),
        ),
    ]