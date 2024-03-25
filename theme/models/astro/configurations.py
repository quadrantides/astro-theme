# coding=utf-8
"""
Created on 2020, May 26th
@author: orion
"""
from django.db import models

from django.utils.translation import gettext_lazy as _

from .tropical import TropicalConfiguration
from .sidereal import SiderealConfiguration


class Configuration(models.Model):

    configuration_tropical = \
        models.ForeignKey(
            TropicalConfiguration,
            blank=True,
            null=True,
            on_delete=models.CASCADE,
            verbose_name="configuration tropicale",
        )

    configuration_sidereal = \
        models.ForeignKey(
            SiderealConfiguration,
            blank=True,
            null=True,
            on_delete=models.CASCADE,
            verbose_name="configuration sidérale",
        )

    class Meta:
        app_label = 'theme'

    def get(self):
        return dict(
            tropical=self.configuration_tropical.get(),
            sidereal=self.configuration_sidereal.get(),
        )

    def __str__(self):
        res1 = self.configuration_tropical.__str__()
        res2 = self.configuration_sidereal.__str__()

        return ", ".join(
            [res1, res2],
        )
