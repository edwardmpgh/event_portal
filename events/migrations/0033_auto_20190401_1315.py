# Generated by Django 2.1.5 on 2019-04-01 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0032_auto_20190401_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
