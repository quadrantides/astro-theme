# coding=utf-8
"""
Created on 2020, May 15th
@author: orion
"""

from django import forms
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
# from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab

from theme.models import Theme
from astro import generics


# class NewThemeForm(MyMultiModelForm):
#     class Meta:
#         model = [BirthForm, AstrologiesParametersForm]
#         # exclude = ('moderations',)
#         # widgets = {'text': forms.Textarea(attrs={'cols': 100, 'rows': 10}),
#         #            'tags': forms.Textarea(attrs={'cols': 100, 'rows': 1})}
#         # labels = {'tags': _(u"Mots-clés"), }
#         # help_texts = {'tags': _(u"Liste servant à référencer vos textes. Séparez chaque mot-clé par une virgule."),
#         #               }


class CelebritiesForm(forms.ModelForm):
    celebrity = forms.CharField(
        label="",
        # required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nos thèmes, par exemple : Emmanuel Macron'}),
    )
    selected_celebrity_pk = forms.IntegerField()

    class Meta:
        model = Theme
        exclude = ('first_name', "last_name", "birth", "context")

    def __init__(self, *args, **kwargs):
        super(CelebritiesForm, self).__init__(*args, **kwargs)
        self.fields['selected_celebrity_pk'].widget = forms.HiddenInput()
        self.helper = FormHelper()
        # self.helper.form_action = reverse('theme:celebrity', kwargs={'pk': self.instance.pk})
        # self.helper.form_class = 'form-inline'
        # self.helper.label_class = 'col-md-4'
        # self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            Row(
                "selected_celebrity_pk",
                Column(
                    'celebrity',
                    css_class="col-md-9",
                ),
                Column(
                    Submit('submit', 'AFFICHER', css_class="btn btn-default"),
                    css_class="col-md-3",
                ),
                css_class="col-md-12",
            )

        )


# def get_default_model_name(model):
#
#     name = u"get_default_model_name"
#     model_name = ""
#
#     try:
#         item = model.objects.get(default=True)
#     except model.DoesNotExist as e:
#         success = False
#         code = e.__class__.__name__
#         message = e.message
#     except model.MultipleObjectsReturned as e:
#         success = False
#         code = e.__class__.__name__
#         message = e.message
#     else:
#         model_name = item.code
#         success, code, message = generics.returned_code_ok()
#
#     return generics.ReturnedCode(name, success, code, message), model_name


# def get_model_choices(model):
#     name = u"get_sidereal_modes_as_choices"
#     choices = []
#     try:
#         items = model.objects.all()
#     except model.DoesNotExist as e:
#         success = False
#         code = e.__class__.__name__
#         message = e.message
#     else:
#         for item in items:
#             choices.append(
#                 (item.code, item.name),
#             )
#         success, code, message = generics.returned_code_ok()
#
#     return generics.ReturnedCode(name, success, code, message), choices
