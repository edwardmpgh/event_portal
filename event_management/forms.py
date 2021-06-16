from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Button, HTML, ButtonHolder, Field, Fieldset, Hidden
from crispy_forms.bootstrap import FormActions, FieldWithButtons, StrictButton, InlineCheckboxes

from events.models import Event, Attendee, StoreFront


# add a new event
class NewEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name',
                  'location_name',
                  'location_address',
                  'location_map_url',
                  'url',
                  'start_date',
                  'start_time',
                  'end_time',
                  'signup_start',
                  'signup_by',
                  'description',
                  'refund_policy',
                  'confirmation_text',
                  'contact_name',
                  'contact_email',
                  'event_form',
                  'storefront',
                  'storefront_itemcode',
                  'fee',
                  'max_capacity',
                  'allowed_guest',
                  'group',
                  'show_form_only',
                  #'show_registration_barcode',
                  ]

    def __init__(self, *args, **kwargs):
        super(NewEventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form form-vertical'
        self.helper.form_method = 'post'
        self.fields['name'].help_text = 'Title of Event'
        self.fields['location_name'].help_text = 'Ex. Hamburg Hall'
        self.fields['location_address'].help_text = 'Street Address'
        self.fields['contact_name'].help_text = 'Event organizer name who will answer event questions'
        self.fields['contact_email'].help_text = 'Event organizer email who will receive questions about the event'
        #self.fields['show_registration_barcode'].help_text = 'Indicates if the registration confirmation should show a barcode for the registration ID. Use this if checking in participants with a barcode reader.'
        self.fields['url'].help_text = 'What will appear in the URL for the event. Alphanumeric characters only and no spaces. DO NOT ADD https://heinz.cmu.edu, THE SYSTEM WILL DO THAT FOR YOU. Example: URL for your event is Pirates_summer_1 the URL will appear as: https://event.heinz.cmu.edu/events/event/Pirates_summer_1'
        self.fields['storefront'].help_text = 'Select your storefront. If it does not exist, email heinz-computing@andrew.cmu.edu'
        self.fields['storefront_itemcode'].help_text = 'Unique ID for your event in the storefront. Contact heinz-computing@andrew.cmu.edu for this code'
        self.fields['group'].help_text = 'Select an group who can access this event. Contact heinz-computing@andrew.cmu.edu to request a new group'
        self.fields['fee'].help_text = 'This is what you are charging to attend the event.'
        self.fields['max_capacity'].help_text = 'Zero means unlimited capacity.'
        self.fields['allowed_guest'].help_text = 'Number of guests an attendee can bring to the event.'
        self.fields['signup_start'].help_text = 'Blank signup start date means signup is open immediately.'
        self.fields['signup_by'].help_text = 'Sign up date assumes Pittsburgh timezone.'
        self.fields['event_form'].help_text = 'Click help in the header for form information'
        self.fields['show_form_only'].help_text = 'Do not show event details, just the event title, signup by date, fee, and form'
        self.fields['signup_start'].widget.attrs = {'id': 'datepicker', 'data-provide': 'datepicker'}
        self.fields['start_date'].widget.attrs = {'id': 'datepicker', 'data-provide': 'datepicker'}
        self.fields['signup_by'].widget.attrs = {'id': 'datepicker', 'data-provide': 'datepicker'}
        self.fields['start_time'].widget.attrs = {'id': 'time1', 'data-format': "h:mm A", 'class': 'input-small'}
        self.fields['end_time'].widget.attrs = {'id': 'time2', 'data-format': "h:mm A", 'class': 'input-small'}
        self.helper.layout = Layout(
            Fieldset(
                'Event Information',
                'name',
                'location_name',
                'location_address',
                'location_map_url',
                'description',
                'confirmation_text',
                'refund_policy',
                #'show_registration_barcode',
                'start_date',
                'start_time',
                'end_time',
                'signup_start',
                'signup_by',
            ),
            Fieldset(
                'Event Settings',
                'contact_name',
                'contact_email',
                'url',
                'event_form',
                'show_form_only',
            ),
            Fieldset(
                'Event Capacity',
                'max_capacity',
                'allowed_guest',
            ),
            Fieldset(
                'Storefront Information - SEE HEINZ COMPUTING BEFORE USING THIS SECTION',
                'storefront',
                'storefront_itemcode',
                'fee',
            ),
            Fieldset(
                'Access Control',
                'group',
            ),
        )

# add a new storefront
class StorefrontForm(ModelForm):
    class Meta:
        model = StoreFront
        fields = ['name',
                  'storefront_url',
                  ]

    def __init__(self, *args, **kwargs):
        super(StorefrontForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form form-vertical col-6'
        self.helper.form_method = 'post'
        self.fields['storefront_url'].help_text = 'https://commerce.cashnet.com/404Handler/pageredirpost.aspx?virtual=[storefront id]'
        self.helper.layout = Layout(
                'name',
                'storefront_url',
        )
