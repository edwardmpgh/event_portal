# Generated by Django 2.1.5 on 2019-01-25 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('trash', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=255)),
                ('registration_number', models.UUIDField()),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('dietary_needs', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('registration_date', models.DateTimeField(blank=True, null=True)),
                ('registration_fee', models.IntegerField(blank=True, null=True)),
                ('registration_paid', models.IntegerField(blank=True, null=True)),
                ('email_sent', models.DateField(blank=True, null=True)),
                ('transaction_number', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'hz_evetns_attendee',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('trash', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=20, unique=True)),
                ('start_date', models.DateField()),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('signup_by', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('contact_name', models.CharField(blank=True, max_length=75, null=True)),
                ('contact_email', models.CharField(max_length=255)),
                ('event_image', models.FileField(blank=True, null=True, upload_to='')),
                ('fee', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'hz_evetns_event',
                'ordering': ['start_date', 'name'],
            },
        ),
        migrations.CreateModel(
            name='EventForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('trash', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=50)),
                ('form_name', models.CharField(max_length=50)),
                ('form_image', models.FileField(blank=True, null=True, upload_to='')),
            ],
            options={
                'db_table': 'hz_evetns_event_form',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='StoreFront',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('trash', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=50)),
                ('storefront_url', models.CharField(blank=True, max_length=255, null=True)),
                ('storefront_itemcode', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='event',
            name='event_form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.EventForm'),
        ),
        migrations.AddField(
            model_name='event',
            name='storefront',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.StoreFront'),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendee',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.Event'),
        ),
    ]