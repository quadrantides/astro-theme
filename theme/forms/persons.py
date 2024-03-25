# coding=utf-8
"""
Created on 2020, May 20th
@author: orion
"""
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Layout, Row, Column

from astro.utils import Person


from django import forms


class LatLonField(forms.FloatField):

    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return float(value)


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = "__all__"

    def __init__(self, *args, **kwargs):

        super(PersonForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = 'id-person-form'
        self.helper.layout = Layout(

            Row(
                Column(
                    'first_name', css_class="col-md-3",
                ),
                Column(
                    'last_name', css_class="col-md-3",
                ),
                Column(
                    'further_information', css_class="col-md-6",
                ),
                css_class="col-md-12",
            ),
        )
