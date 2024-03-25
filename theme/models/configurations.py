# coding=utf-8
"""
Created on 2020, May 12th
@author: orion
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Configuration(models.Model):

    active = \
        models.BooleanField(
            default=False,
            verbose_name="afficher ?",
        )

    default = \
        models.BooleanField(
            default=False,
            verbose_name="est la configuration par défaut ?",
        )

    class Meta:
        app_label = 'theme'
        abstract = True

    def __str__(self):
        return "active = {}, est la configuration par défaut ? = {}".format(
            self.active,
            self.default,
        )
