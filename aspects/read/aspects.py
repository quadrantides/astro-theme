# coding=utf-8
"""
Created on 2020, June 11th
@author: orion
"""
from django.db.models import F

from astro import generics
from astro.utils import is_conjunction


from aspects.models import validate_angle
from aspects.models import get_aspect_model, get_conjunction_model

from aspects.read.cycles import get as get_cycle
from aspects.read.orbs import get as get_orb


def get_all_orb(cycle, angle, orb, start, end, conjunction_type=""):

    name = u"get_all_orb_aspect"
    code = ""
    message = ""
    success = False
    obj = None
    cycle_name = cycle.get_name()
    aspect_model = get_aspect_model(cycle_name)

    if is_conjunction(angle) and cycle.is_internal:
        conjunction_model = get_conjunction_model(cycle_name)
        try:
            obj = conjunction_model.objects.filter(
                type=conjunction_type,
                active=False,
                aspect__cycle=cycle.id,
                aspect__orb=orb.id,
                aspect__start__gte=start,
                aspect__end__lte=end,
            )

            success = True

        except conjunction_model.DoesNotExist as e:
            code = e.__class__.__name__
            message = ", ".join(e.args)
        else:
            if success:
                success, code, message = generics.returned_code_ok()
    else:
        try:
            obj = aspect_model.objects.filter(
                cycle=cycle.id,
                angle=angle,
                orb=orb.id,
                start__gte=start,
                end__lte=end,
            )

            success = True

        except aspect_model.DoesNotExist as e:
            code = e.__class__.__name__
            message = ", ".join(e.args)
        else:
            if success:
                success, code, message = generics.returned_code_ok()

    return generics.ReturnedCode(name, success, code, message), obj


def _get_all(cycle, angle, start, end, conjunction_type=""):

    name = u"_get_all_aspect"
    code = ""
    message = ""
    success = False
    obj = None

    try:
        obj = model.objects.filter(
            cycle=cycle.id,
            angle=angle,
            start__gte=start,
            end__lte=end,
        )

        success = True

    except model.DoesNotExist as e:
        code = e.__class__.__name__
        message = ", ".join(e.args)
    else:
        if success:
            success, code, message = generics.returned_code_ok()

    return generics.ReturnedCode(name, success, code, message), obj


def get_all(cycle, angle, start, end, orb_value=None, conjunction_type=""):
    name = u"get_all_aspect"
    obj = None

    if orb_value:
        rc, orb = get_orb(orb_value)
        if rc.success:
            rc, obj = get_all_orb(cycle, angle, orb, start, end, conjunction_type=conjunction_type)
    else:
        rc, obj = _get_all(cycle, angle, start, end, conjunction_type=conjunction_type)

    return rc, obj


def get(planet1, planet2, angle, start, end, orb_value=None, conjunction_type=""):

    name = u"get_aspect"

    success = False
    obj = None

    rc, cycle = get_cycle(planet1, planet2)

    if rc.success:
        rc, obj = \
            get_all(
                cycle,
                validate_angle(angle),
                start,
                end,
                orb_value=orb_value,
                conjunction_type=conjunction_type,
            )
    else:
        code = ", ".join(rc.code)
        message = ", ".join(rc.message)
        rc = generics.ReturnedCode(name, success, code, message), obj

    return rc, obj


def get_id(model, id):

    name = u"get_id"
    code = ""
    message = ""
    success = False
    obj = None

    try:
        obj = model.objects.get(
            aspect=id,
        )
        success = True

    except model.DoesNotExist as e:
        code = e.__class__.__name__
        message = ", ".join(e.args)
    else:
        if success:
            success, code, message = generics.returned_code_ok()

    return generics.ReturnedCode(name, success, code, message), obj


def get_internal_conjunctions(planet1, planet2, aspect_id):

    name = u"get_internal_conjunctions"

    obj = None

    rc, cycle = get_cycle(planet1, planet2)

    if rc.success:
        cycle_name = cycle.get_name()
        model = get_conjunction_model(cycle_name)
        rc, obj = get_id(model, aspect_id)

    return rc, obj
