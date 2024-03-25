# coding=utf-8
"""
Created on 2020, June 19th
@author: orion
"""
from astro import generics

from aspects.models import Cycle2

from aspects.read.planets import get as get_planet


def _get(planet1, planet2):

    name = u"_get_cycle"
    code = ""
    message = ""
    obj = None
    success = False
    try:
        obj = Cycle2.objects.get(planet1=planet1.id, planet2=planet2.id)
        success = True
    except Cycle2.DoesNotExist as e:
        code = e.__class__.__name__
        message = ", ".join(e.args)
    else:
        if success:
            success, code, message = generics.returned_code_ok()

    return generics.ReturnedCode(name, success, code, message), obj


def get(planet1, planet2):

    name = u"get_cycle"

    success = False
    obj = None

    rc1, planet1 = get_planet(planet1)
    rc2, planet2 = get_planet(planet2)

    if rc1.success and rc2.success:
        rc, obj = _get(planet1, planet2)
        if not rc.success:
            rc, obj = _get(planet2, planet1)
    else:
        codes = []
        messages = []
        if not rc1.success:
            codes.append(rc1.code)
            messages.append(rc1.message)
        if not rc2.success:
            codes.append(rc2.code)
            messages.append(rc2.message)
        code = ", ".join(codes)
        message = ", ".join(messages)
        rc = generics.ReturnedCode(name, success, code, message)

    return rc, obj
