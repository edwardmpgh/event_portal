import datetime
import time

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.template.loader import get_template
from django.template import Context

from events.models import Attendee


class Command(BaseCommand):

    help = 'Send email to all registrations that have note received a message'

    def handle(self, *args, **options):
        attendee = Attendee.objects.get(id=37)

        event = attendee.event

        # email fields
        email_subject = 'Registration Confirmation for %s' % event.name
        email_from = event.contact_email
        email_to = attendee.email

        # plain text and HTML email templates
        plain_text_part = get_template('events/email.txt')
        html_part = get_template('events/email.html')

        # confirmation information needed to fill in templates
        context = dict(
            event=event,
            registration=attendee,
            balance=attendee.registration_fee-attendee.registration_paid
        )

        # render the templates with the confirmation information
        text_content = plain_text_part.render(context)
        html_content = html_part.render(context)

        # build the email message and send it
        msg = EmailMultiAlternatives(email_subject, text_content, email_from, [email_to,])
        #msg.attach_alternative(html_content, 'text/html')
        msg.send(fail_silently=True)
