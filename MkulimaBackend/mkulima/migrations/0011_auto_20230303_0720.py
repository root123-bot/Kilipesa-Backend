# Generated by Django 3.2 on 2023-03-03 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0010_auto_20230303_0637'),
    ]

    operations = [
        migrations.AddField(
            model_name='gatherprofile',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
        migrations.AddField(
            model_name='gatherprofile',
            name='education_level',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='gatherprofile',
            name='user_group',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
