# Generated by Django 2.0.3 on 2018-05-12 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_appinfo_currentversion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrecord',
            name='timeInfo',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
