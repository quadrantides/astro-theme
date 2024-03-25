# coding=utf-8
"""
Created on 2020, May 12th
@author: orion
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class SiderealMode(models.Model):

    name = models.CharField(max_length=150, verbose_name="Sidereal mode, as human readable name")
    code = models.CharField(max_length=150, verbose_name="Sidereal code fof the mode", default="")
    default = models.BooleanField(
        verbose_name="Is default name ?",
        default=False,
    )

    class Meta:
        app_label = 'theme'

    def __str__(self):
        return "{}".format(
            self.name,
        )
