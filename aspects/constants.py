# coding=utf-8
"""
Created on 2020, June 9th
@author: orion
"""
import os
from django.utils.translation import ugettext as _

ASPECTS_OUTPUTS = os.environ["ASPECTS_OUTPUTS"]

ASPECTS_OUTPUTS_HTML = os.path.join(
    ASPECTS_OUTPUTS,
    "HTML",
)

ASPECTS = [
    _('conjunction'),
    _('semi-sextile'),
    _('semi-square'),
    _('sextile'),
    _('quintile'),
    _('square'),
    _('sesquiquadrate'),
    _('biquintile'),
    _('quincunx'),
    _('opposition'),
    _('trine'),
]

SORTED_ASPECTS = [
    'conjunction',
    'semi-sextile',
    'sextile',
    'semi-square',
    'square',
    'quintile',
    'trine',
    'sesquiquadrate',
    'quincunx',
    'biquintile',
    'opposition',
]

DEFAULT_ORBS = {
    'conjunction': 10,
    'semi-sextile': 4,
    'semi-square': 4,
    'sextile': 4,
    'quintile': 2,
    'square': 6,
    'trine': 8,
    'sesquiquadrate': 4,
    'biquintile': 2,
    'quincunx': 4,
    'opposition': 10,
}


def get_default_orb(aspect_name):
    value = -1.0
    if aspect_name in DEFAULT_ORBS.keys():
        value = DEFAULT_ORBS[aspect_name]
    return value
