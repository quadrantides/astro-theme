# coding=utf-8
"""
Created on 2020, May 12th
@author: orion
"""
from django.utils import timezone

from theme.models import Birth, Theme

if __name__ == '__main__':

    birth = Birth(
        date=timezone.datetime(1977, 12, 21, 10, 40),
        location="Amiens",
        latitude=2.3,
        longitude=49.9,
        altitude=25.0,
        time_zone='Europe/Paris',
        context="80, Somme, Hauts-de-France",
    )
    birth.save()

    theme = Theme(
        first_name='Emmanuel',
        last_name="Macron",
        birth=birth,
        context=""
    )
    theme.save()
