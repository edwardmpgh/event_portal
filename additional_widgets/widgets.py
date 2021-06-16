from django.forms import widgets

# note: use {{form.media}} in template to load JS and CSS
# If using crsipy forms, this will happen automatically


class RadioWithOther(widgets.RadioSelect):

    class Media:
        js = ['js/option_text_input.js']


class OtherFieldForMultiSelect(widgets.TextInput, radio_id=None):

    class Media:
        js = ['additional_widgets/js/option_text_input.js']
