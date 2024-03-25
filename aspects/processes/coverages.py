# -*- coding: utf-8 -*-
"""
Created on 2020, June 9th
@author: orion

"""
from astro import generics
from aspects.models import Planet
from aspects.models import Cycle2
from aspects.models import Coverage
from aspects.models import Orb


def filter(model, planet1, planet2, angle, orb):

    name = u"get_default_model_name"
    qs = None

    try:
        planet1 = Planet.objects.get(name=planet1)
        planet2 = Planet.objects.get(name=planet2)
        cycle = Cycle2.objects.get(planet1=planet1.id, planet2=planet2.id)
        orb = Orb.objects.get(value=float(orb))
        qs = model.objects.filter(cycle=cycle.id, angle=float(angle), orb=orb.id)

    except model.DoesNotExist as e:
        success = False
        code = e.__class__.__name__
        message = e.__str__()
    except model.MultipleObjectsReturned as e:
        success = False
        code = e.__class__.__name__
        message = e.__str__()
    else:
        success, code, message = generics.returned_code_ok()

    return generics.ReturnedCode(name, success, code, message), qs


def exists(model, planet1, planet2, angle, orb, time_range):
    res = False
    rc, coverage = filter(model, planet1, planet2, angle, orb)
    if rc.success:
        for item in coverage:
            condition1 = item.start < time_range[0] < item.end
            condition2 = item.start < time_range[1] < item.end
            if condition1 or condition2:
                raise Exception(
                    "La base de données contient déjà en totalité ou "
                    "en partie les aspects liés à la demande en cours : "
                    "START DATE : {} - END DATE : {} - "
                    "ANGLE : {} - ORB : {}".format(
                        time_range[0],
                        time_range[1],
                        angle,
                        orb,
                    ),
                )

    return res
    # return False
