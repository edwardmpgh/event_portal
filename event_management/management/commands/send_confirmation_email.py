import datetime
import time

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.template.loader import get_template

from events.models import Attendee


class Command(BaseCommand):

    help = 'Send email to all registrations that have note received a message'

    def handle(self, *args, **options):
        self.stdout.write('send emails: %s' % timezone.now())

        # get a list of new attendees that have no received an email confirmation
        new_registrations = Attendee.objects.filter(email_sent__isnull=True, active=True, trash=False)
        # print("Number of new emails: %s" % new_registrations.count())

        if new_registrations:
            # send emails to each new attendee
            for registration in new_registrations:
                print('Emailing: %s' % registration.email)

                # check if there is a fee for the event
                send_email = True
                if registration.event.fee:
                    # don't send confirmation to folks that have not paid yet
                    if not registration.registration_paid:
                        send_email = False

                if send_email:
                    # email = EmailMessage(
                    #     'Registration Confirmation for %s' % registration.event.name,
                    #     get_email_body(registration),
                    #     'no-reply@andrew.cmu.edu',
                    #     [registration.email, ],
                    #     [registration.event.contact_email, ],
                    #     reply_to=[registration.event.contact_email],
                    #     headers={'Message-ID': registration.registration_number},
                    # )
                    # registration.email_sent = datetime.date.today()
                    # registration.save()
                    # time.sleep(1)
                    # email.send()

                    # get the event object from the registration record
                    event = registration.event

                    # email fields
                    email_subject = 'Registration Confirmation for %s' % event.name
                    email_from = event.contact_email
                    email_to = registration.email

                    # assign the email templates
                    plain_text_part = get_template('events/email.txt')
                    html_part = get_template('events/email.html')

                    context = dict(
                        event=event,
                        registration=registration,
                        balance=registration.registration_fee - registration.registration_paid
                    )

                    # render hte email templates with the attendee information
                    text_content = plain_text_part.render(context)
                    html_content = html_part.render(context)

                    # send the email
                    msg = EmailMultiAlternatives(email_subject, text_content, email_from, [email_to, ])
                    msg.attach_alternative(html_content, 'text/html')
                    msg.send(fail_silently=True)
                    registration.email_sent = datetime.date.today()
                    registration.save()

                    # wait a second so we don't overwhelm the email server
                    time.sleep(1)
