# coding=utf-8
"""
Created on 2020, May 12th
@author: orion
"""
from django.template.context_processors import csrf
from django.http import JsonResponse

from crispy_forms.utils import render_crispy_form

from theme.forms.locations import LocationForm
from transcend.views.geoname import get as get_geoname_location


def default_view(request):
    success = False
    if request.method == "POST":
        form = LocationForm(request.POST or None)
        if form.is_valid():
            success = True
            location = form.cleaned_data
            geoname_location = get_geoname_location(
                location["latitude"],
                location["longitude"],
            )
            location['time_zone'] = geoname_location['timezone']

            if geoname_location['countrycode'] != 'FR':
                location['city'] = geoname_location['city']
                location['context'] = "Pays : {}, Continent : {}".format(
                    geoname_location['countrycode'],
                    geoname_location['continent'],
                )
        else:
            location = dict()
    return JsonResponse(
        {'success': success, "message": "", 'location': location},
    )
