# coding=utf-8
"""
Created on 2020, May 20th
@author: orion
"""
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML

from theme.models import Location

from django import forms


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        exclude = ("creation", "last_update")
        # fields = "__all__"
        widgets = dict(
            latitude=forms.NumberInput(attrs={'size': 20}),
            longitude=forms.NumberInput(attrs={'size': 20}),
            altitude=forms.NumberInput(attrs={'size': 20}),
        )

    def __init__(self, *args, **kwargs):

        super(LocationForm, self).__init__(*args, **kwargs)

        # self.fields["time_zone"].disabled = True
        self.fields["latitude"].localize = True
        self.fields["longitude"].localize = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = 'id-location-form'
        self.helper.layout = Layout(
            Row(
                HTML("<h6>Lieu de naissance</h6>"),
                Column(
                    'city', css_class="col-md-4",
                ),
                Column(
                    Row(
                        'context', css_class="col-md-12",
                    ),
                    Row(
                        Column(
                            'latitude', css_class="col-md-4",
                        ),

                        Column(
                            'longitude', css_class="col-md-4",
                        ),
                        Column(
                            'altitude', css_class="col-md-4",
                        ),
                        css_class="col-md-12",
                    ),

                    Row(
                        Column(
                            'time_zone', css_class="col-md-12",
                        ),
                    ),
                    css_class="col-md-8",
                ),
                css_class="col-md-12",
            ),
            # Column(
            #     Row(
            #         Column(
            #             'city', css_class="col-md-5",
            #         ),
            #         Column(
            #             Row(
            #                 'context', css_class="col-md-12",
            #             ),
            #             Row(
            #                 'latitude', css_class="col-md-12",
            #             ),
            #             Row(
            #                 'longitude', css_class="col-md-12",
            #             ),
            #             Row(
            #                 'altitude', css_class="col-md-12",
            #             ),
            #             Row(
            #                 'time_zone', css_class="col-md-12",
            #             ),
            #             css_class="col-md-7",
            #         ),
            #         css_class="col-md-12",
            #     ),
            #
            #     css_class="col-md-6 border-left-0",
            # ),
            # Column(
            #     HTML(
            #         "Si le lieu de naissance se situe hors de France, cliquez sur la localité",
            #     ),
            #     # Div(
            #     #     Div(
            #     #         # 'map',
            #     #         css_id="map"
            #     #     ),
            #     #     css_class="div-leaflet-map",
            #     # ),
            #     css_class="col-md-6",
            # ),
        )
