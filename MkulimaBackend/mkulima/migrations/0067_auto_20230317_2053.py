# Generated by Django 3.2 on 2023-03-17 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0066_alter_gatheredinfo_gathered_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nextkeen',
            name='country',
        ),
        migrations.RemoveField(
            model_name='nextkeen',
            name='district',
        ),
        migrations.RemoveField(
            model_name='nextkeen',
            name='region',
        ),
        migrations.RemoveField(
            model_name='nextkeen',
            name='street',
        ),
        migrations.RemoveField(
            model_name='nextkeen',
            name='ward',
        ),
    ]