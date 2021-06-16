# Generated by Django 2.1.5 on 2019-02-21 19:17

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_event_confirmation_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='confirmation_text',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]