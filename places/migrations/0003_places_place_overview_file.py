# Generated by Django 3.1.6 on 2021-02-27 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_auto_20210223_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='place_overview_file',
            field=models.FileField(null=True, upload_to='documents/'),
        ),
    ]
