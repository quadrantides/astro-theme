# coding=utf-8
"""
Created on 2020, June 19th
@author: orion
"""
from aspects.models import Orb
from astro import generics


def get(value):
    name = u"get_orb"
    code = ""
    message = ""
    success = False
    obj = None

    try:
        obj = Orb.objects.get(value=value)
        success = True
    except Orb.DoesNotExist as e:
        code = e.__class__.__name__
        message = ", ".join(e.args)
    else:
        if success:
            success, code, message = generics.returned_code_ok()

    return generics.ReturnedCode(name, success, code, message), obj
