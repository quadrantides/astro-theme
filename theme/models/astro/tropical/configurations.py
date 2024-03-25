# coding=utf-8
"""
Created on 2020, May 26th
@author: orion
"""
from django.utils.translation import gettext_lazy as _

from theme.models.configurations import Configuration as BaseConfiguration
from theme.models.astro.tropical.parameters import Parameters


class TropicalConfiguration(BaseConfiguration, Parameters):

    class Meta:
        app_label = 'theme'

    def __str__(self):
        string1 = BaseConfiguration.__str__(self)
        string2 = Parameters.__str__(self)
        return ", ".join(
            [string1, string2],
        )
