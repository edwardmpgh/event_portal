from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='admin_index'),
    path('access/', views.request_access, name='request_access'),
    path('event/new/', views.new_event, name='new_event'),
    path('event/edit/<int:event_id>', views.edit_event, name='edit_event'),
    path('event/status/change/<int:event_id>', views.change_event_status, name='change_event_status'),
    path('event/details/<int:event_id>', views.event_details, name='event_details'),
    path('event/trash/<int:event_id>', views.event_trash, name='event_trash'),
    path('event/storefront/list', views.storefront_list, name='storefront_list'),
    path('event/storefront/status/<int:storefront_id>', views.change_storefront_status, name='change_storefront_status'),
    path('event/storefront/new', views.new_storefront, name='new_storefront'),
    path('event/storefront/edit/<int:storefront_id>', views.edit_storefront, name='edit_storefront'),
    path('event/storefront/trash/<int:storefront_id>', views.storefront_trash, name='storefront_trash'),
    path('event/attendees/<int:event_id>', views.attendee_list, name='attendee_list'),
    path('event/attendees/download/<int:event_id>', views.download_attendee_csv, name='download_attendee_csv'),
    path('event/attendees/status/<int:attendee_id>', views.change_attendee_status, name='change_attendee_status'),
    path('event/attendees/trash/<int:attendee_id>', views.attendee_trash, name='attendee_trash'),
]
