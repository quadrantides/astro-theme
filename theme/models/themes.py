# coding=utf-8
"""
Created on 2020, May 12th
@author: orion
"""
from django.utils.timezone import now
from django.db import models

from astro.utils import Timestamp
from astro.utils import Person


class Location(Timestamp, models.Model):

    city = models.CharField(
        max_length=150,
        verbose_name="Ville",
        default="Paris",
    )

    latitude = models.FloatField(
        verbose_name="latitude",
        default=48.8534,
    )

    longitude = models.FloatField(
        verbose_name="longitude",
        default=2.3488,
    )

    altitude = models.FloatField(
        verbose_name="altitude",
        default=25.0,
    )

    time_zone = models.CharField(
        max_length=80,
        verbose_name="fuseau horaire",
        default="Europe/Paris",
        blank=True,
    )

    context = models.CharField(
        max_length=120,
        verbose_name="contexte",
        default="75, Paris, Île-de-France",
        blank=True,
    )

    class Meta:
        app_label = 'theme'

    def __str__(self):
        return "Ville = {}, Latitude = {}, Longitude = {}, Contexte = {}, Fuseau horaire = {}".format(
            self.city,
            self.latitude,
            self.longitude,
            self.context,
            self.time_zone,

        )


class Date(models.Model):

    date = models.DateTimeField(
        verbose_name="date",
        default=now,
    )

    class Meta:
        abstract = True
        app_label = 'theme'

    def __str__(self):
        return "Date = {}".format(
            self.date,

        )


class Theme(Timestamp, Person, Date, models.Model):

    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="localisation")

    ordering = ['full_name']

    class Meta:
        app_label = 'theme'

    # def get_absolute_url(self):
    #     """Returns the url to access a particular instance of the model."""
    #     return reverse('theme-detail-view', args=[str(self.id)])

    def __str__(self):
        res1 = Person.__str__(self)
        res2 = Date.__str__(self)
        # res3 = ", Localisation = {}".format(self.location)
        return ", ".join([res1, res2])
