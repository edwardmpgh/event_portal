# Generated by Django 2.2 on 2019-04-08 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0035_auto_20190408_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='return_from_payment_portal',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
