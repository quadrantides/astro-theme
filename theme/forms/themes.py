# coding=utf-8
"""
Created on 2020, May 16th
@author: orion
"""
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML

from theme.models import Theme as ThemeModel
from theme.models import Date as ThemeDateModel

from django import forms


# class LatLonField(forms.FloatField):
#
#     def to_python(self, value):
#         """Normalize data to a list of strings."""
#         # Return an empty list if no input was given.
#         if not value:
#             return []
#         return float(value)


class Theme(forms.ModelForm):

    class Meta:
        model = ThemeModel
        exclude = ("creation", "last_update")

    def __init__(self, *args, **kwargs):

        super(Theme, self).__init__(*args, **kwargs)


class Date(forms.ModelForm):

    class Meta:
        model = ThemeDateModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        super(Date, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = 'id-date-form'
        self.helper.layout = Layout(
            HTML('<input type="hidden" id="id_date_hidden" name="date" value="{{ date }}">'),
            # HTML('<input type="hidden" id="id_transit_date_hidden" name="date" value="{{ date }}">'),
        )
