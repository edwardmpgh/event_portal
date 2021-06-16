from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Button, HTML, ButtonHolder, Field, Fieldset, Hidden
from crispy_forms.bootstrap import FormActions, FieldWithButtons, StrictButton, InlineCheckboxes

from events.models import Attendee, AFFILIATION_CHOICES


def get_guest_choices(event):

    return [(o, str(o)) for o in range(0, event.allowed_guest+1)]


# The form that contains the necessary information to hand off to Cashnet for payment
class CashnetHandoffForm(ModelForm):
    class Meta:
        model = Attendee
        fields = [
            'first_name',
            'last_name',
            'email',
            'registration_number',
            'registration_fee',
            'itemcode',
            'custcode',
            'amount',
        ]

    # custom fields needed for Cashnet
    custcode = forms.IntegerField()
    amount = forms.IntegerField()
    itemcode = forms.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super(CashnetHandoffForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form form-vertical'
        self.helper.form_method = 'post'
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            HTML(
                'Thank you for registering. You will now be forwarded to our payment vendor to complete registration.'),
            Field('registration_number', type='hidden'),
            Field('first_name', type='hidden'),
            Field('last_name', type='hidden'),
            Field('email', type='hidden'),
            Field('registration_fee', type='hidden'),
            Field('amount', type='hidden'),
            Field('itemcode', type='hidden'),
            Field('custcode', type='hidden'),
            ButtonHolder(
                Submit('submit', 'Continue to Payment Portal', css_class='btn btn-outline-danger')
            ),
        )

#######################################
# Signup form section                 #
# Forms in the section are for event  #
# signup                              #
#######################################


class SimpleSignupForm(ModelForm):
    class Meta:
        model = Attendee
        fields = [
            'first_name',
            'last_name',
            'email',
        ]

    def __init__(self, *args, **kwargs):
        super(SimpleSignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form form-vertical'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'phone',
        )


class SimplePlusSignupForm(ModelForm):
    class Meta:
        model = Attendee
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
        ]

    def __init__(self, *args, **kwargs):
        super(SimplePlusSignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form form-vertical'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'phone',
        )


class SimpleSignupDietForm(ModelForm):
    class Meta:
        model = Attendee
        fields = [
            'first_name',
            'last_name',
            'email',
            'dietary_needs',
        ]

    def __init__(self, *args, **kwargs):
        super(SimpleSignupDietForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form form-vertical'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'phone',
            'dietary_needs',
        )


class FullSignupForm(ModelForm):
    class Meta:
        model = Attendee
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'guests',
            'guests_name',
        ]

    def __init__(self, *args, **kwargs):
        super(FullSignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form form-vertical'
        self.helper.form_method = 'post'
        # set the number of guests in the dropdown
        self.fields['guests'].widget = forms.Select(choices=get_guest_choices(self.instance.event))
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'phone',
            'guests',
            'guests_name',
        )


class NameOrgTitleComment(ModelForm):
    class Meta:
        model = Attendee
        fields = [
            'first_name',
            'last_name',
            'title',
            'organization',
            'email',
            'comment',
        ]

    def __init__(self, *args, **kwargs):
        super(NameOrgTitleComment, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form form-vertical'
        self.helper.form_method = 'post'
        # set the number of guests in the dropdown
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'title',
            'organization',
            'email',
            'comment',
        )


class SimpleSignupWithAffiliationForm(ModelForm):
    class Meta:
        model = Attendee
        fields = [
            'first_name',
            'last_name',
            'email',
            'affiliation',
            'affiliation_other',
        ]

    class Media:
        js = ['js/option_text_input.js']

    def __init__(self, *args, **kwargs):
        super(SimpleSignupWithAffiliationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form form-vertical'
        self.helper.form_method = 'post'
        self.fields['affiliation'].widget = forms.RadioSelect(choices=AFFILIATION_CHOICES)
        self.fields['affiliation_other'].widget = forms.TextInput(attrs={'placeholder': 'Enter Affiliation', 'class': 'display-on'})
        self.fields['affiliation_other'].label = ''
        self.fields['affiliation_other'].initial = ''
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'affiliation',
            'affiliation_other',
        )

    def clean(self):
        data = self.cleaned_data
        affiliation = data['affiliation']
        affiliation_other = data['affiliation_other']
        if affiliation and affiliation == 'Other':
            if not affiliation_other:
                msg = forms.ValidationError("This field is required.")
                self.add_error('affiliation_other', msg)
                self.fields['affiliation_other'].widget = forms.TextInput(attrs={'placeholder': 'Enter Affiliation', 'class': 'display-on'})
        return self.cleaned_data


class NameEmailTypeAffiliation(ModelForm):
    class Meta:
        model = Attendee
        fields = [
            'first_name',
            'last_name',
            'email',
            'registration_type',
        ]

    def __init__(self, *args, **kwargs):
        super(NameEmailTypeAffiliation, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form form-vertical'
        self.helper.form_method = 'post'
        # self.fields['registration_type'].widget = ListTextWidget(data_list=REGISTRATION_TYPE, name='Type')
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'registration_type',
        )


class HeinzAlumniEvent(ModelForm):
    class Meta:
        model = Attendee
        fields = [
            'first_name',
            'last_name',
            'street_1',
            'street_2',
            'city',
            'state',
            'zip_code',
            'email',
            'phone',
            'heinz_degree_program',
            'graduation_year',
            'guests',
            'guests_name',
        ]

    def __init__(self, *args, **kwargs):
        super(HeinzAlumniEvent, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form form-vertical'
        self.helper.form_method = 'post'
        # set the number of guests in the dropdown
        self.fields['guests'].widget = forms.Select(choices=get_guest_choices(self.instance.event))
        # required fields
        self.fields['street_1'].required = True
        self.fields['city'].required = True
        self.fields['state'].required = True
        self.fields['zip_code'].required = True
        self.fields['phone'].required = True
        self.fields['heinz_degree_program'].required = True
        self.fields['graduation_year'].required = True
        self.fields['guests_name'].help_text = 'Please list guest full name(s) and indicate if they are alumni'
        self.fields['guests_name'].name = 'Guest Name(s)'
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            Div(
                Div('heinz_degree_program', css_class='col-md-8', ),
                Div('graduation_year', css_class='col-md-4', ),
                css_class='row',
            ),
            Fieldset(
                'Mailing Address',
                'street_1',
                'street_2',
                'city',
                'state',
                'zip_code',
            ),
            Fieldset(
                'Contact Information',
                'phone',
                'email',
            ),
            Fieldset(
                'Guests',
                'guests',
                'guests_name',
            ),
        )

    def clean(self):
        data = self.cleaned_data
        guests = data['guests']
        guests_name = data['guests_name']
        if guests > 0:
            if not guests_name:
                msg = forms.ValidationError("This field is required.")
                self.add_error('guests_name', msg)
                self.fields['guests_name'].widget = forms.TextInput(
                    attrs={'placeholder': 'Enter guest name'})
        return self.cleaned_data


class HeinzAlumniEventShort(ModelForm):
    class Meta:
        model = Attendee
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'heinz_degree_program',
            'graduation_year',
            'guests',
            'guests_name',
        ]

    def __init__(self, *args, **kwargs):
        super(HeinzAlumniEventShort, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form form-vertical'
        self.helper.form_method = 'post'
        # set the number of guests in the dropdown
        self.fields['guests'].widget = forms.Select(choices=get_guest_choices(self.instance.event))
        # required fields
        self.fields['phone'].required = True
        self.fields['heinz_degree_program'].required = True
        self.fields['graduation_year'].required = True
        self.fields['guests_name'].help_text = 'Please list guest full name(s) and indicate if they are alumni'
        self.fields['guests_name'].name = 'Guest Name(s)'
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            Div(
                Div('heinz_degree_program', css_class='col-md-8', ),
                Div('graduation_year', css_class='col-md-4', ),
                css_class='row',
            ),
            Fieldset(
                'Contact Information',
                'phone',
                'email',
            ),
            Fieldset(
                'Guests',
                'guests',
                'guests_name',
            ),
        )

    def clean(self):
        data = self.cleaned_data
        guests = data['guests']
        guests_name = data['guests_name']
        if guests > 0:
            if not guests_name:
                msg = forms.ValidationError("This field is required.")
                self.add_error('guests_name', msg)
                self.fields['guests_name'].widget = forms.TextInput(
                    attrs={'placeholder': 'Enter guest name'})
        return self.cleaned_data
