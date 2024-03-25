# coding=utf-8
"""
Created on 2020, May 27th
@author: orion
"""

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Column, Div, Row

from theme.models.astro.sidereal.configurations import SiderealConfiguration
from theme.models.astro.tropical.configurations import TropicalConfiguration

from astro import generics


class SiderealConfigurationForm(forms.ModelForm):

    class Meta:
        model = SiderealConfiguration
        exclude = ('active', 'default')

    def __init__(self, *args, **kwargs):
        super(SiderealConfigurationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-sidereal-configuration-form'
        self.helper.layout = Layout(
            Div(
                Column('houses_system', css_class='col-md-3'),
                Column('mode', css_class='col-md-3'),
                Submit('submit', 'APPLIQUER', css_class='col-md-2 btn btn-primary'),

                css_class='align-selection-group',
            ),
        )


class TropicalConfigurationForm(forms.ModelForm):

    class Meta:
        model = TropicalConfiguration
        exclude = ('active', 'default')

    def __init__(self, *args, **kwargs):
        super(TropicalConfigurationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-tropical-configuration-form'
        self.helper.layout = Layout(
            Div(
                Column('houses_system', css_class='col-md-3'),
                Submit('submit', 'APPLIQUER', css_class='col-md-2 btn btn-primary'),

                css_class='align-selection-group',
            ),
        )


def get_default_model_name(model):

    name = u"get_default_model_name"
    model_name = ""

    try:
        item = model.objects.get(default=True)
    except model.DoesNotExist as e:
        success = False
        code = e.__class__.__name__
        message = e.message
    except model.MultipleObjectsReturned as e:
        success = False
        code = e.__class__.__name__
        message = e.message
    else:
        model_name = item.code
        success, code, message = generics.returned_code_ok()

    return generics.ReturnedCode(name, success, code, message), model_name


def get_model_choices(model):
    name = u"get_sidereal_modes_as_choices"
    choices = []
    try:
        items = model.objects.all()
    except model.DoesNotExist as e:
        success = False
        code = e.__class__.__name__
        message = e.message
    else:
        for item in items:
            choices.append(
                (item.code, item.name),
            )
        success, code, message = generics.returned_code_ok()

    return generics.ReturnedCode(name, success, code, message), choices


# class AccountCreationForm(CombinedFormBase):
#     form_classes = [TropicalParametersForm]


# class SettingsForm(CombinedFormBase):
#     class Meta:
#         model = [UserForm, ProfileForm]
#         exclude = ('moderations',)
#         widgets = {'text': forms.Textarea(attrs={'cols': 100, 'rows': 10}),
#                    'tags': forms.Textarea(attrs={'cols': 100, 'rows': 1})}
#         labels = {'tags': _(u"Mots-clés"), }
#         help_texts = {'tags': _(u"Liste servant à référencer vos textes. Séparez chaque mot-clé par une virgule."),
#                       }
