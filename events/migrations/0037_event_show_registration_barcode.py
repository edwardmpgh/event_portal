# Generated by Django 2.2 on 2019-04-09 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0036_attendee_return_from_payment_portal'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='show_registration_barcode',
            field=models.BooleanField(default=False),
        ),
    ]
