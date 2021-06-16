import datetime

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField

from heinz_signup.settings import MEDIA_ROOT, DATE_INPUT_FORMATS

DB_PREFIX = 'hz_events_'


class CommonField(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    trash = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @property
    def is_active(self):
        return self.active

    @property
    def is_trash(self):
        return self.trash

    def flip_active_flag(self):
        if self.active:
            self.active = False
        else:
            self.active = True

    def flip_trash_flag(self):
        if self.trash:
            self.trash = False
        else:
            self.trash = True


class EventForm(CommonField):
    name = models.CharField(max_length=50)
    form_name = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = DB_PREFIX + 'event_form'
        ordering = ['name']


class StoreFront(CommonField):
    name = models.CharField(max_length=50)
    storefront_url = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = DB_PREFIX + 'store_front'
        ordering = ['name']


allowed_guest_choices = (
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
)


class ManagementGroup(CommonField):
    name = models.CharField(max_length=50)
    members = models.TextField()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = DB_PREFIX + 'management_group'
        ordering = ['name']


class Event(CommonField):
    # validator for url - alphnumeric, dash, underscore only)
    alphanumeric = RegexValidator(r'^[A-Za-z0-9_-]+$',
                                  'Only alphanumeric, dash, and underscore characters are allowed.')

    name = models.CharField(max_length=110)
    url = models.CharField(max_length=20, unique=True, validators=[alphanumeric])
    start_date = models.DateField()
    start_time = models.TimeField(max_length=12)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(max_length=12, blank=True, null=True)
    location_name = models.CharField(max_length=200)
    location_address = models.CharField(max_length=500)
    location_map_url = models.CharField(max_length=1000, blank=True, null=True)
    signup_start = models.DateField(blank=True, null=True)
    signup_by = models.DateField(blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    confirmation_text = RichTextField(blank=True, null=True)
    refund_policy = RichTextField(blank=True, null=True)
    contact_name = models.CharField(max_length=75)
    contact_email = models.EmailField(max_length=255)
    event_image = models.ImageField(upload_to='', blank=True, null=True)
    event_form = models.ForeignKey(EventForm, on_delete=models.PROTECT,
                                   limit_choices_to={'active': True, 'trash': False})
    storefront = models.ForeignKey(StoreFront, on_delete=models.SET_NULL, blank=True, null=True,
                                   limit_choices_to={'active': True, 'trash': False})
    storefront_itemcode = models.CharField(max_length=50, blank=True, null=True)
    fee = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    group = models.ForeignKey(ManagementGroup, on_delete=models.SET_NULL, blank=True, null=True)
    max_capacity = models.IntegerField(default=0)
    allowed_guest = models.IntegerField(default=0, choices=allowed_guest_choices)
    show_registration_barcode = models.BooleanField(default=False)
    show_form_only = models.BooleanField(default=False)

    def __str__(self):
        return '%s: %s' % (self.name, self.start_date)

    class Meta:
        db_table = DB_PREFIX + 'event'
        ordering = ['start_date', 'name']

    @property
    def get_total_collected(self):
        return Attendee.objects.filter(active=True, trash=False, event=self).annotate(Sum('registration_paid'))

    @property
    def get_total_attendee_count(self):

        # get count of attendees
        attendees = Attendee.objects.filter(active=True, trash=False, event=self)
        attendee_count = attendees.count()
        # get count of guests
        guest_count = attendees.aggregate(models.Sum('guests'))
        # calculate total attendance
        if guest_count['guests__sum'] is None:
            guest_count['guests__sum'] = 0

        attendee_total_count = attendee_count + guest_count['guests__sum']

        return attendee_total_count

    @property
    def is_at_capacity(self):
        # assume the event is full
        at_capacity = True

        attendee_total_count = self.get_total_attendee_count

        # zero means unlimited capacity, or attendee count has not reached max capacity
        if self.max_capacity == 0 or attendee_total_count < self.max_capacity:
            at_capacity = False

        return at_capacity

    @property
    def is_signup_open(self):
        event_open = True
        if self.signup_start:
            if self.signup_start >= timezone.now().date():
                event_open = False
        if self.signup_by:
            if self.signup_by <= timezone.now().date():
                event_open = False

        return event_open

    # @property
    # def is_past_signup_by_date(self):
    #     if self.signup_by >= timezone.now().date():
    #         return False
    #     else:
    #         return True
    #
    # @property
    # def is_today_signup_date(self):
    #     if self.signup_by == timezone.now().date():
    #         return True
    #     else:
    #         return False


guest_choices_0 = [
    (0, '0'),
]

guest_choices_1 = [
    (0, '0'),
    (1, '1'),
]

guest_choices_2 = [
    (0, '0'),
    (1, '1'),
    (2, '2'),
]

guest_choices_3 = [
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
]

guest_choices_4 = [
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
]

REGISTRATION_TYPE_CHOICES = (
    ('Current Student', 'Student'),
    ('Alumni', 'Alumni'),
    ('Faculty', 'Faculty'),
    ('Staff', 'Staff'),
    ('Admitted Heinz Student', 'Admitted Heinz Student'),
    ('Prospective Heinz Student', 'Prospective Heinz Student'),
)

AFFILIATION_CHOICES = (
    ('College of Engineering', 'College of Engineering'),
    ('College of Fine Arts', 'College of Fine Arts'),
    ('Dietrich College of Humanities & Social Sciences', 'Dietrich College of Humanities & Social Sciences'),
    ('Heinz College of Information Systems and Public Policy','Heinz College of Information Systems and Public Policy'),
    ('Mellon College of Science', 'Mellon College of Science'),
    ('School of Computer Science', 'School of Computer Science'),
    ('Tepper School of Business', 'Tepper School of Business'),
    ('Other', 'Other'),
)


class Attendee(CommonField):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=200, blank=True, null=True)
    organization = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    registration_number = models.UUIDField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    guests = models.IntegerField(default=0, choices=guest_choices_4) # set choices to max number allowed
    guests_name = models.CharField(max_length=500, blank=True, null=True, verbose_name='Guest Name(s)')
    dietary_needs = models.CharField(max_length=50, default='', blank=True, null=True)
    registration_date = models.DateTimeField(blank=True, null=True)
    registration_fee = models.IntegerField(blank=True, null=True)
    registration_paid = models.IntegerField(blank=True, null=True)
    return_from_payment_portal = models.DateTimeField(blank=True, null=True)
    email_sent = models.DateField(blank=True, null=True)
    transaction_number = models.CharField(max_length=255, blank=True, null=True)
    registration_type = models.CharField(max_length=30, default='Other', choices=REGISTRATION_TYPE_CHOICES)
    registration_type_other = models.CharField(max_length=30, blank=True, null=True)
    affiliation = models.CharField(max_length=150, default='Other', choices=AFFILIATION_CHOICES)
    affiliation_other = models.CharField(max_length=150, blank=True, null=True)
    heinz_degree_program = models.CharField(max_length=255, blank=True, null=True)
    graduation_year = models.CharField(max_length=4, blank=True, null=True)
    street_1 = models.CharField(max_length=255, blank=True, null=True)
    street_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s: %s, %s' % (self.event.name, self.last_name, self.first_name)

    class Meta:
        db_table = DB_PREFIX + 'attendee'
        ordering = ['last_name', 'first_name']

ELEMENT_TYPE_CHOICES = (
    ('CharField', 'Alphanumeric'),
    ('IntegerField', 'Integer'),
    ('TextField', 'Text Field'),
    ('BooleanField', 'Check Box'),
    ('DateField', 'Date'),
)


# models for managing signup form elements
class FormElements(CommonField):
    name = models.CharField(max_length=30)
    label = models.CharField(max_length=30)
    element_type = models.CharField(max_length=50, choices=ELEMENT_TYPE_CHOICES)
    element_choices = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = DB_PREFIX + 'form_elements'
        ordering = ['name']


class CustomForm(CommonField):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = DB_PREFIX + 'custom_form'
        ordering = ['name']


class CustomFormFields(CommonField):
    custom_form = models.ForeignKey(CustomForm, on_delete=models.CASCADE)
    field_type = models.ForeignKey(FormElements, on_delete=models.PROTECT)
    label = models.CharField(max_length=30)
    field_size = models.ImageField(default=10)
    required = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.custom_form

    class Meta:
        db_table = DB_PREFIX + 'custom_form_fields'
        ordering = ['custom_form']
