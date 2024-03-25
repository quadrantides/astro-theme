# coding=utf-8
"""
Created on 2020, May 21th
@author: orion
"""
from theme.models import Location
from astro import generics

DECIMAL_PRECISION = 4


def get(data):
    name = u"get_location"
    obj = None
    kwargs = dict(
        latitude=round(
            data['latitude'],
            DECIMAL_PRECISION,
        ),
        longitude=round(
            data['longitude'],
            DECIMAL_PRECISION,
        ),
    )
    try:
        qs = Location.objects.filter(**kwargs)
        if len(qs) > 0:
            obj = qs[0]

    except Location.DoesNotExist as e:
        success = False
        code = e.__class__.__name__
        message = e.message
    else:
        success, code, message = generics.returned_code_ok()

    return generics.ReturnedCode(name, success, code, message), obj
