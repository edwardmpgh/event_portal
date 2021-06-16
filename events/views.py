from uuid import uuid4

from django.shortcuts import render, get_object_or_404, redirect, reverse, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone

from .models import Event, Attendee
from .forms import SimplePlusSignupForm, SimpleSignupForm, FullSignupForm, NameEmailTypeAffiliation, \
    CashnetHandoffForm, SimpleSignupWithAffiliationForm, HeinzAlumniEvent, HeinzAlumniEventShort, NameOrgTitleComment, \
    SimpleSignupDietForm

# this is a list of forms that are available for event owners to use for event signup
# these forms must be defined in events.forms
form_list = dict(
    SimplePlusSignupForm=SimplePlusSignupForm,
    SimpleSignupForm=SimpleSignupForm,
    SimpleSignupWithAffiliationForm=SimpleSignupWithAffiliationForm,
    FullSignupForm=FullSignupForm,
    NameEmailTypeAffiliation=NameEmailTypeAffiliation,
    HeinzAlumniEvent=HeinzAlumniEvent,
    HeinzAlumniEventShort=HeinzAlumniEventShort,
    NameOrgTitleComment=NameOrgTitleComment,
    SimpleSignupDietForm=SimpleSignupDietForm,
)


# override default error handlers
def handler404(request, exception, template_name="404.html"):
    response = render_to_response("404.html")
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response("500.html")
    response.status_code = 500
    return response


# redirect anyone that hits the root of the website to the Heinz College main event website
def index(request):

    # redirect root access to the Heinz website event page
    return HttpResponseRedirect('https://www.heinz.cmu.edu/events/#category=Featured%20Events&pageIndex=0&pageSize=9')


# display the details for an event
# requires an event.url
def event_detail(request, event_url):

    context = dict(title='Heinz Event Signup',
                   app_page='events',
                   page='events',
                   form_title='Registration',
                   )

    # get the event information or show a 404 error
    event = get_object_or_404(Event, url=event_url, active=True, trash=False)
    # create a new attendee object and generate a UUID4 and set the event
    instance = Attendee()
    instance.registration_number = uuid4()
    instance.event = event

    # check if the request is a form post
    if request.method == 'POST':
        # get the form information from the request object
        form = form_list[event.event_form.form_name](request.POST or None, instance=instance)
        if form.is_valid():
            # save the information before we do anything else.
            form.save()

            # check if there is a fee
            if event.fee:
                # calculate cost
                total_attendees = instance.guests + 1
                total_cost = total_attendees * event.fee
                # save the cost information
                instance.registration_fee = total_cost
                instance.registration_paid = 0
                instance.registration_date = timezone.now()
                instance.save()
                # send to the payment confirmation page
                return HttpResponseRedirect(reverse('paymnet_handoff', args=(instance.registration_number,)))
            else:
                # no fee so send them to the confirmation page
                instance.registration_fee = 0
                instance.registration_paid = 0
                instance.registration_date = timezone.now()
                instance.save()
                return HttpResponseRedirect(reverse('event_confirmation', args=(instance.registration_number,)))
        else:
            # there were errors, add the errors to the error section of the return page
            messages.error(request, form.errors)
    else:
        # it is a GET event, create a new form and attach to the new attendee object
        form = form_list[event.event_form.form_name](instance=instance)

    context['form'] = form
    context['event'] = event
    context['button_title'] = 'Continue'

    # show the event information and form
    return render(request, 'events/generic_event_form.html', context)


# the event requires payment so generate a hand off form for Cashnet
# requires attendee.registration_number
def paymnet_handoff(request, registration_number):

    context = dict(title='Heinz Event Signup',
                   app_page='event',
                   page='payment',
                   header_title='Heinz Events',
                   form_title='Payment Confirmation',
                   )

    # get the attendee object
    registration_instance = get_object_or_404(Attendee, registration_number=registration_number)
    # crate a new Cashnet hand off form and set its values equal to the attendee object
    form = CashnetHandoffForm(request.POST or None, instance=registration_instance)
    # cashnet required field data
    form.fields['amount'].initial = registration_instance.registration_fee
    form.fields['itemcode'].initial = registration_instance.event.storefront_itemcode
    form.fields['custcode'].initial = registration_instance.id

    context['form'] = form
    context['storefront_url'] = registration_instance.event.storefront.storefront_url
    context['event'] = registration_instance.event
    context['total_attendee'] = registration_instance.guests + 1
    context['total_cost'] = registration_instance.registration_fee

    # show the payment page
    return render(request, 'events/handoff.html', context)

# show a successful event registration
# requires attendee.registration_number
#      When None: attendee is coming back to the site from Cashnet (reg number is in custcode)
@csrf_exempt
def event_confirmation(request, registration_number=None):

    context = dict(title='Heinz Event Signup',
                   app_page='event',
                   page='confirmation',
                   header_title='Heinz Events',
                   form_title='Confirmation',
                   )

    # the the request is a POST, it is a return from Cashnet. Check that custcode is in the request
    if request.method == 'POST' and 'custcode' in request.POST:
        # get the attendee object or show an error
        registration_instance = get_object_or_404(Attendee, id=request.POST['custcode'])
        # update the registration record
        registration_instance.registration_paid = registration_instance.registration_fee
        registration_instance.transaction_number = request.POST['tx']
        registration_instance.return_from_payment_portal = timezone.now()
        registration_instance.save()
    elif request.method == 'GET':
        # this is a event that does not require a fee, get the attendee info
        registration_instance = get_object_or_404(Attendee, registration_number=registration_number)
    else:
        # todo give error message
        registration_instance = get_object_or_404(Attendee, registration_number=registration_number)

    # show the registration confirmation information
    context['registration'] = registration_instance
    context['balance'] = registration_instance.registration_fee - registration_instance.registration_paid
    context['event'] = registration_instance.event

    # show the user their registration confirmation
    return render(request, 'events/confirmation.html', context)


# this is an old function that was incorporated into the confirmation function
def event_payment_complete(request, registration_number):
    context = dict(title='Heinz Event Signup',
                   app_page='event',
                   page='paymnet',
                   header_title='Heinz Events',
                   form_title='Payment Complete',
                   )

    attendee_instance = get_object_or_404(Attendee, registration_number=registration_number)

    form = CashnetHandoffForm(request.POST or None, instance=attendee_instance)

    # Cashnet will use the amount field for the value to charge the CC
    form.fields['amount'].initial = attendee_instance.registration_fee
    form.fields['itemcode'].initial = attendee_instance.event.storefront_itemcode
    form.fields['custcode'].initial = attendee_instance.id
    print(form)
    context['form'] = form
    context['event'] = attendee_instance.event

    return render(request, 'events/handoff.html', context)
