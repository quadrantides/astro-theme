# coding=utf-8
"""
Created on 2020, May 19th
@author: orion
"""
from theme.models import Theme
from astro import generics


def get_by_id(id):
    name = u"get_theme"
    success = False
    obj = None
    try:
        obj = Theme.objects.get(id=id)
        success = True
    except Theme.DoesNotExist as e:
        code = e.__class__.__name__
        message = e.message
    else:
        success, code, message = generics.returned_code_ok()

    return generics.ReturnedCode(name, success, code, message), obj


def get_by_keys(data):
    name = u"get_theme"
    obj = None
    kwargs = dict(
        last_name=data['last_name'],
        first_name=data['first_name'],
        further_information=data['further_information'],
    )
    try:
        qs = Theme.objects.filter(**kwargs)
        if len(qs) > 0:
            obj = qs[0]
    except Theme.DoesNotExist as e:
        success = False
        code = e.__class__.__name__
        message = e.message
    else:
        success, code, message = generics.returned_code_ok()

    return generics.ReturnedCode(name, success, code, message), obj
