# Generated by Django 3.2 on 2023-03-14 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0060_auto_20230313_1951'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='Administrator', max_length=50, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('user_group', models.CharField(default='Admin', max_length=200)),
            ],
        ),
    ]