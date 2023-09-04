# Generated by Django 3.2 on 2023-03-08 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mkulima', '0042_auto_20230306_0717'),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(blank=True, max_length=800, null=True)),
                ('region', models.CharField(blank=True, max_length=800, null=True)),
                ('district', models.CharField(blank=True, max_length=800, null=True)),
                ('ward', models.CharField(blank=True, max_length=800, null=True)),
                ('street', models.CharField(blank=True, max_length=800, null=True)),
                ('size', models.CharField(blank=True, help_text='Size in hectras', max_length=800, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='farm',
            name='country',
            field=models.CharField(blank=True, max_length=800, null=True),
        ),
        migrations.AddField(
            model_name='farm',
            name='district',
            field=models.CharField(blank=True, max_length=800, null=True),
        ),
        migrations.AddField(
            model_name='farm',
            name='region',
            field=models.CharField(blank=True, max_length=800, null=True),
        ),
        migrations.AddField(
            model_name='farm',
            name='size',
            field=models.CharField(blank=True, help_text='Size in hectras', max_length=800, null=True),
        ),
        migrations.AddField(
            model_name='farm',
            name='street',
            field=models.CharField(blank=True, max_length=800, null=True),
        ),
        migrations.AddField(
            model_name='farm',
            name='ward',
            field=models.CharField(blank=True, max_length=800, null=True),
        ),
    ]