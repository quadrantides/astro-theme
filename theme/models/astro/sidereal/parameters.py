# coding=utf-8
"""
Created on 2020, May 12th
@author: orion
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..houses import HousesSystem
from .modes import SiderealMode


class Parameters(models.Model):

    houses_system = \
        models.ForeignKey(
            HousesSystem,
            on_delete=models.CASCADE,
            verbose_name="système de maisons",
        )

    mode = \
        models.ForeignKey(
            SiderealMode,
            on_delete=models.CASCADE,
            verbose_name="mode",
        )

    class Meta:
        app_label = 'theme'
        abstract = True

    def get(self):
        return dict(
            houses_system=self.houses_system,
            mode=self.mode,
        )

    def __str__(self):
        string1 = "système de maison = {}".format(
            self.houses_system
        )
        string2 = ", mode = {}".format(self.mode)
        return ", ".join([string1, string2])
