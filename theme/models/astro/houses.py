# coding=utf-8
"""
Created on 2020, May 12th
@author: orion
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class HousesSystem(models.Model):

    name = models.CharField(max_length=150, verbose_name="Houses system, as human readable name")
    code = models.CharField(max_length=1, verbose_name="Houses system code", default="")
    default = models.BooleanField(
        verbose_name="Système par défaut ?",
        default=False,
    )

    class Meta:
        app_label = 'theme'

    def __str__(self):
        return "{}".format(
            self.name,
        )
