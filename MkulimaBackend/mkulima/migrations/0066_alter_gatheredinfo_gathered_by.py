# Generated by Django 3.2 on 2023-03-16 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0065_alter_adminprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gatheredinfo',
            name='gathered_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gathered_by', to='mkulima.gatherprofile'),
        ),
    ]
