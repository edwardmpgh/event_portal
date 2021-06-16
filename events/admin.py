from django.contrib import admin

from .models import Event, EventForm, Attendee, StoreFront, ManagementGroup

admin.site.register(Event)
admin.site.register(EventForm)
admin.site.register(Attendee)
admin.site.register(StoreFront)
admin.site.register(ManagementGroup)
