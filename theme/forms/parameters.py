# coding=utf-8
"""
Created on 2020, May 14th
@author: orion
"""

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Column, Div, Row

from theme.models.astro.houses import HousesSystem
from theme.models.astro.parameters import Parameters as AstrologiesParameters
from theme.models.astro.tropical.parameters import Parameters as TropicalParameters
from theme.models.astro.sidereal.parameters import Parameters as SiderealParameters

from theme.models import HousesSystem
from theme.models import SiderealMode
from astro import generics


class SiderealParametersForm(forms.ModelForm):

    class Meta:
        model = SiderealParameters
        exclude = ('active', 'default')

    def __init__(self, *args, **kwargs):
        super(SiderealParametersForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-sidereal-parameters-form'
        self.helper.layout = Layout(
            Div(
                Column('houses_system', css_class='col-md-3'),
                Column('mode', css_class='col-md-3'),
                Submit('submit', 'APPLIQUER', css_class='col-md-2 btn btn-primary'),

                css_class='align-selection-group',
            ),
        )


class HousesSystemsForm(forms.ModelForm):

    class Meta:
        model = HousesSystem
        exclude = ('code',)

    def __init__(self, *args, **kwargs):
        super(HousesSystemsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-houses-system-form'
        self.helper.layout = Layout(
            Column('name', css_class='col-md-3'),
            Submit('submit', 'APPLIQUER', css_class='col-md-2 btn btn-primary'),
        )


class TropicalForm(forms.Form):

    houses_system = forms.ModelChoiceField(
        queryset=HousesSystem.objects.all(),
        empty_label=None,
        label="Système des maisons",
    )

    def __init__(self, *args, **kwargs):
        super(TropicalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = "GET"
        self.helper.form_id = 'id-tropical-houses-system-form'
        self.helper.layout = Layout(
            Div(
                Column('houses_system'),
                # Submit('submit', 'APPLIQUER', css_class='col-md-2 btn btn-primary'),

                css_class='align-selection-group',
            ),
        )


class SiderealForm(forms.Form):

    houses_system = forms.ModelChoiceField(
        queryset=HousesSystem.objects.all(),
        empty_label=None,
        label="Système des maisons",
    )

    mode = forms.ModelChoiceField(
        queryset=SiderealMode.objects.all(),
        empty_label=None,
        label="mode",
    )

    def __init__(self, *args, **kwargs):
        super(SiderealForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = 'id-sidereal-parameters-form'
        self.helper.layout = Layout(
            Row(
                Column('houses_system', css_class='col-md-6'),
                Column('mode', css_class='col-md-6'),
                css_class='align-selection-group',
            ),
        )


class TropicalParametersForm(forms.ModelForm):
    class Meta:
        model = TropicalParameters
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(TropicalParametersForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-tropical-parameters-form'
        self.helper.layout = Layout(
            Div(
                Column('houses_system', css_class='col-md-3'),
                Submit('submit', 'APPLIQUER', css_class='col-md-2 btn btn-primary'),

                css_class='align-selection-group',
            ),
        )


class AstrologiesParametersForm(forms.ModelForm):

    tropical_houses_system = forms.ChoiceField(choices=[("None", "None")], label="Tropical")
    sidereal_houses_system = forms.ChoiceField(choices=[("None", "None")], label="Sidéral")
    sidereal_modes = forms.ChoiceField(choices=[("None", "None")], label="Modes")

    class Meta:
        model = AstrologiesParameters
        exclude = ('tropical', "sidereal",)

    def __init__(self, *args, **kwargs):
        input = kwargs.pop('tropical_houses_system_input', None)
        super(AstrologiesParametersForm, self).__init__(*args, **kwargs)
        rc, result = get_model_choices(HousesSystem)
        if rc.success:
            self.fields["tropical_houses_system"].widget = forms.Select(choices=result)
            self.fields["sidereal_houses_system"].widget = forms.Select(choices=result)

        rc, result = get_default_model_name(HousesSystem)
        if rc.success:
            self.fields["tropical_houses_system"].initial = result
            self.fields["sidereal_houses_system"].initial = result
        rc, result = get_model_choices(SiderealMode)
        if rc.success:
            self.fields["sidereal_modes"].widget = forms.Select(choices=result)

        rc, result = get_default_model_name(SiderealMode)
        if rc.success:
            self.fields["sidereal_modes"].initial = result
        self.helper = FormHelper()
        # self.helper.form_class = 'form-inline'
        # self.helper.label_class = 'col-md-6'
        # self.helper.field_class = 'col-md-4'
        self.helper.layout = Layout(
            Div(
                Column('tropical_houses_system', css_class='col-md-2'),
                Column('sidereal_houses_system', css_class='col-md-2'),
                Column('sidereal_modes', css_class='col-md-2'),
                Submit('submit', 'APPLIQUER', css_class='col-md-1 btn btn-primary'),

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
