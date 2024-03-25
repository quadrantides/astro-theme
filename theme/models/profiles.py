# coding=utf-8
"""
Created on 2020, May 26th
@author: orion
"""
from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _

from astro.utils import Timestamp
from theme.models.astro.configurations import Configuration
# from theme.models.configurations import Configuration


class Profile(Timestamp, Configuration, models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        app_label = 'theme'

    def __str__(self):
        res = Configuration.__str__(self)

        return ", ".join([res])
