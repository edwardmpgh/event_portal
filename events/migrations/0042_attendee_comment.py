# Generated by Django 2.2 on 2019-04-16 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0041_attendee_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
