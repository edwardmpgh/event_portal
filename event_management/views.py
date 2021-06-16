import datetime
from uuid import uuid4
import csv
from itertools import chain

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail

from events.models import Event, Attendee, StoreFront
from .forms import NewEventForm, StorefrontForm


# show a list of events
@login_required(redirect_field_name='target')
@staff_member_required
def index(request):

    current_user = request.user

    context = dict(title='Event Management Panel',
                   page='index',
                   app_page='management',
                   fullname=current_user.first_name + ' ' + current_user.last_name,
                   )

    # get events that the user owns and get events with groups the user is a member of
    events = Event.objects.filter(trash=False, user=current_user).order_by('start_date') | Event.objects.filter(trash=False, group__members__contains=current_user).order_by('start_date')

    context['events'] = events

    return render(request, 'event_management/index.html', context)


# page for a user to request access to the event system
@login_required
def request_access(request):

    current_user = request.user

    context = dict(title='Event Management Panel',
                   app_page='management',
                   page='request_access',
                   fullname=current_user.first_name + ' ' + current_user.last_name,
                   )

    email_sent = True

    if current_user.is_staff:
        # the person already has access, send them to the index page
        return HttpResponseRedirect(reverse('admin_index'))
    else:
        # email the access request to the help desk
        try:
            send_mail(
                'Event portal access requested',
                'The following user has requested access to the Heinz event portal: %s' % current_user.username,
                'nheinz-computing@andrew.cmu.edu',
                ['heinz-computing@andrew.cmu.edu'],
                fail_silently=True,
            )
            email_sent = True
        except:
            email_sent = False

        context['email_sent'] = email_sent

        return render(request, 'event_management/request_access.html', context)


# create a new event
@login_required
@staff_member_required
def new_event(request):

    current_user = request.user

    context = dict(title='Event Management Panel',
                   app_page='management',
                   page='new_event',
                   fullname=current_user.first_name + ' ' + current_user.last_name,
                   )

    # set the event form
    form = NewEventForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            # save the new event and send user to the index page
            f = form.save(commit=False)
            f.user = current_user
            form.save()
            return HttpResponseRedirect(reverse('admin_index'))
        else:
            # send the error message to the user
            messages.error(request, form.errors)

    context['form'] = form
    context['form_title'] = 'Add a New Event'
    context['button_title'] = 'Add'

    return render(request, 'event_management/generic_form.html', context)


# edit an existing event
@login_required
@staff_member_required
def edit_event(request, event_id):

    current_user = request.user

    context = dict(title='Event Management Panel',
                   app_page='management',
                   page='new_event',
                   fullname=current_user.first_name + ' ' + current_user.last_name,
                   )
    # create an instance of the event from the event_id parameter
    instance = get_object_or_404(Event, id=event_id)
    # create a new form and fill it in with the instance data
    form = NewEventForm(request.POST or None, request.FILES or None, instance=instance)

    if request.method == 'POST':
        if form.is_valid():
            # save the new event and send user to the index page
            form.save()
            return HttpResponseRedirect(reverse('admin_index'))
        else:
            # send the error message to the user
            messages.error(request, form.errors)

    context['form'] = form
    context['form_title'] = 'Edit Event'
    context['button_title'] = 'Change'

    return render(request, 'event_management/generic_form.html', context)


# change the active status of the event
@login_required
@staff_member_required
def change_event_status(request, event_id):

    # create an instance of the event from the event_id parameter or show a 404 error
    instance = get_object_or_404(Event, id=event_id)
    # use the model function to flip the active flag
    instance.flip_active_flag()
    instance.save()
    return HttpResponseRedirect(reverse('admin_index'))


# show the details of an event
@login_required
@staff_member_required
def event_details(request, event_id):

    current_user = request.user

    context = dict(title='Event Management Panel',
                   app_page='management',
                   page='event_details',
                   fullname=current_user.first_name + ' ' + current_user.last_name,
                   )

    # create an instance of the event from the event_id parameter or show a 404 error
    context['event'] = get_object_or_404(Event, id=event_id)

    return render(request, 'event_management/event_details.html', context)


# set the trash flag for an event
@login_required
@staff_member_required
def event_trash(request, event_id):

    current_user = request.user

    context = dict(title='Event Management Panel',
                   app_page='management',
                   page='trash_event',
                   fullname=current_user.first_name + ' ' + current_user.last_name,
                   )
    # create an instance of the event from the event_id parameter or show a 404 error
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        if 'cancel' in request.POST:
            # the user decided to cancel trashing the event, take them back to the event index
            return HttpResponseRedirect(reverse('admin_index'))
        else:
            # user confirmed to trash the event
            event.flip_trash_flag()
            event.save()
            return HttpResponseRedirect(reverse('admin_index'))

    # build a confirmation page to double check that the user wants to
    context['confirmation_info'] = 'Do you want to delete: \n\n %s\non: %s %s\n' % (
        event.name,
        event.start_date,
        event.start_time,
    )
    context['button_yes_title'] = 'Yes'
    context['form_title'] = 'Trash Event'

    return render(request, 'event_management/generic_confirm_form.html', context)


# show a list of the configured storefronts
@login_required
@staff_member_required
def storefront_list(request):

    current_user = request.user

    context = dict(title='Event Management Panel',
                   app_page='storefront',
                   page='trash_event',
                   fullname=current_user.first_name + ' ' + current_user.last_name,
                   )

    # get the storefronts
    context['storefronts'] = StoreFront.objects.filter(trash=False)

    return render(request, 'event_management/storefront_list.html', context)


# change the active status for the storefront
@login_required
@staff_member_required
def change_storefront_status(request, storefront_id):

    # create an instance of the storefront form the storefront_id parameter or show a 404 error if not found
    instance = get_object_or_404(StoreFront, id=storefront_id)
    # change the active status
    instance.flip_active_flag()
    instance.save()

    return HttpResponseRedirect(reverse('storefront_list'))


# add a new storefront to the system
@login_required
@staff_member_required
def new_storefront(request):

    current_user = request.user

    context = dict(title='Event Management Panel',
                   app_page='storefront',
                   page='new_storefront',
                   fullname=current_user.first_name + ' ' + current_user.last_name,
                   )

    # create a new storefront form
    form = StorefrontForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            # save the new storefront
            form.save()
            return HttpResponseRedirect(reverse('storefront_list'))
        else:
            # there was an error in the form, show the user the error
            messages.error(request, form.errors)

    context['form'] = form
    context['form_title'] = 'Add a New Storefront'
    context['button_title'] = 'Add'

    return render(request, 'event_management/generic_form.html', context)


# edit a storefront in the database
@login_required
@staff_member_required
def edit_storefront(request, storefront_id):

    current_user = request.user

    context = dict(title='Event Management Panel',
                   app_page='storefront',
                   page='edit_storefront',
                   fullname=current_user.first_name + ' ' + current_user.last_name,
                   )

    # create an instance of the storefront record using the storefront_id parameter or show a 404 error
    instance = get_object_or_404(StoreFront, id=storefront_id)
    # populate the form with the instance data
    form = StorefrontForm(request.POST or None, instance=instance)

    if request.method == 'POST':
        if form.is_valid():
            # save the edits and go to the storefront list page
            form.save()
            return HttpResponseRedirect(reverse('storefront_list'))
        else:
            # there were form errors, show those to the user
            messages.error(request, form.errors)

    context['form'] = form
    context['form_title'] = 'Edit Storefront'
    context['button_title'] = 'Change'

    return render(request, 'event_management/generic_form.html', context)


# mark a storefront record for trash
@login_required
@staff_member_required
def storefront_trash(request, storefront_id):

    current_user = request.user

    context = dict(title='Event Management Panel',
                   app_page='storefront',
                   page='storefront_trash',
                   fullname=current_user.first_name + ' ' + current_user.last_name,
                   )
    # get the storefront record using the storefront_id parameter or show a 404 error
    store = get_object_or_404(StoreFront, id=storefront_id)

    if request.method == 'POST':
        if 'cancel' in request.POST:
            # user user canceled the deletion, take them back to the list
            return HttpResponseRedirect(reverse('storefront_list'))
        else:
            # useer confirmed the deletion, mark the record for trash
            store.flip_trash_flag()
            store.save()
            return HttpResponseRedirect(reverse('storefront_list'))

    # build the confirmation page
    context['confirmation_info'] = 'Do you want to delete: \n\n %s\n%s\n' % (
        store.name,
        store.storefront_url,
    )
    context['button_yes_title'] = 'Yes'
    context['form_title'] = 'Trash Storefront'

    return render(request, 'event_management/generic_confirm_form.html', context)


# show the people who signed up for an event
# requires event.id
@login_required
@staff_member_required
def attendee_list(request, event_id):

    current_user = request.user

    context = dict(title='Event Management Panel',
                   app_page='management',
                   page='attendee_list',
                   fullname=current_user.first_name + ' ' + current_user.last_name,
                   )

    # get the event or show a 404 error page if it does not exist
    event = get_object_or_404(Event, id=event_id)

    # get the people who signed up to the above event
    attendees = Attendee.objects.filter(trash=False, event=event)

    # set the context variables for the event template
    context['event'] = event
    context['attendees'] = attendees
    context['total_attendees'] = event.get_total_attendee_count
    context['total_collected'] = event.get_total_collected

    # show the attendees
    return render(request, 'event_management/attendee_list.html', context)


# mark an attendee to an event as trash
# they will not count against max capacity fot the event nor show up in the lists
# requires attendee.id
@login_required
@staff_member_required
def attendee_trash(request, attendee_id):

    current_user = request.user

    context = dict(title='Event Management Panel',
                   app_page='management',
                   page='attendee_trash',
                   fullname=current_user.first_name + ' ' + current_user.last_name,
                   )

    # get the attendee or show a 404 error page
    attendee = get_object_or_404(Attendee, id=attendee_id)

    # check if the request is a POST event
    # this is a response from the confirmation form
    if request.method == 'POST':
        # check if the user canceled removing the attendee from the event
        if 'cancel' in request.POST:
            # they did cancel, do nothing and go back to the event attendee list
            return HttpResponseRedirect(reverse('attendee_list', args=(attendee.event.id,)))
        else:
            # user confirmed removing the attendee form the event
            attendee.flip_trash_flag()
            attendee.save()
            # attendee was flagged as trash and will not show up in the vent count or list
            # go back to the event attendee page
            return HttpResponseRedirect(reverse('attendee_list', args=(attendee.event.id,)))

    # build the confirmation page info
    context['confirmation_info'] = 'Do you want to delete: \n\n %s %s <%s>\n' % (
        attendee.first_name,
        attendee.last_name,
        attendee.email,
    )
    context['button_yes_title'] = 'Delete'
    context['form_title'] = 'Delete Attendee'

    # show the confirmation form asking user to confirm trashing the attendee
    return render(request, 'event_management/generic_confirm_form.html', context)


# function for creating a CSV file of attendees for an event
def download_attendee_csv(request, event_id):
    # get event
    event = get_object_or_404(Event, id=event_id)
    # create response object for the file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % event.url
    # create the CSV writer
    writer = csv.writer(response)
    # create the header row
    header = Attendee._meta.get_fields()
    # write header
    writer.writerow(header)
    # get the attendees list
    attendees = Attendee.objects.filter(active=True, trash=False, event=event).values_list()
    list_len = len(attendees)
    # check that there are attendees for the event
    if list_len > 0:
        # create a list of attendees
        for attendee in attendees:
            row = []
            for val in attendee:
                row.append(val)
            writer.writerow(row)

    # return a list of attendees
    return response


# change the attendee status for the event
# requires the attendee.id
@login_required
@staff_member_required
def change_attendee_status(request, attendee_id):

    # get the attendee or show a 404 error to the user
    attendee = get_object_or_404(Attendee, id=attendee_id)
    # change attendee status
    attendee.flip_active_flag()
    attendee.save()
    # return user to the event attendee list
    return HttpResponseRedirect(reverse('attendee_list', args=(attendee.event.id,)))
