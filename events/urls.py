from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='event_index'),
    path('event/<str:event_url>', views.event_detail, name='event_detail'),
    path('event/confirmation/', views.event_confirmation, name='event_confirmation'),
    path('event/confirmation/<str:registration_number>', views.event_confirmation, name='event_confirmation'),
    path('event/payment/handoff/<str:registration_number>', views.paymnet_handoff, name='paymnet_handoff'),
    path('event/payment/<str:registration_number>', views.event_payment_complete, name='event_payment_complete'),
]
