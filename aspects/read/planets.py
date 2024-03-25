# coding=utf-8
"""
Created on 2020, June 19th
@author: orion
"""
from aspects.models import Planet

from astro import generics


def get(planet):

    name = u"get_planet"
    success = False
    code = ""
    message = ""
    obj = None

    try:
        obj = Planet.objects.get(name=planet)
        success = True
    except Planet.DoesNotExist as e:
        code = e.__class__.__name__
        message = ", ".join(e.args)
    else:
        if success:
            success, code, message = generics.returned_code_ok()

    return generics.ReturnedCode(name, success, code, message), obj
