# coding=utf-8
"""
Created on 2020, May 12th
@author: orion
"""
from django.utils.timezone import now
from django.db import models
from django.utils.translation import gettext_lazy as _

PRECISION = 0.1


def convert_degrees_minutes(angle):
    degrees = int(angle)
    decimal = angle - degrees
    minutes = int(
        round(
            decimal * 60,
        ),
    )

    return "{}°{:02}'".format(
        degrees,
        minutes,
    )


def convert_degrees_minutes_seconds(angle):
    degrees = int(angle)
    decimal = angle - degrees
    minutes = int(
        decimal * 60,
    )
    reliquat = decimal * 60 - minutes
    seconds = int(
        round(
            reliquat * 60,
        )
    )

    return "{}°{:02}'{:02}''".format(
        degrees,
        minutes,
        seconds,
    )


def str_date_for_filename(date):
    return str(date).replace('-', "").replace(" ", "").replace(":", "")


def merge(source, destination):
    """
    run me with nosetests --with-doctest file.py

    a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
    b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
    merge(b, a) == { 'first' : { 'all_rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
    True
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value

    return destination


def is_conjunction(angle):
    return abs(angle % 360) <= PRECISION


class Timestamp(models.Model):

    creation = models.DateTimeField(default=now)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    # def save(self, *args, **kwargs):
    #     if not self.creation:
    #         self.date_created = datetime.now()
    #     self.date_modified = datetime.now()
    #     super(Timestamp, self).save(*args, **kwargs)

    def __str__(self):
        return "Date de création = {}, Date de dernière mise à jour = {}".format(
            self.creation,
            self.last_update,
        )


class Person(models.Model):

    # person

    first_name = models.CharField('prénom', max_length=30, blank=True)
    last_name = models.CharField('nom', max_length=150)

    further_information = models.CharField(max_length=80, verbose_name="information complémentaire", blank=True)

    class Meta:
        abstract = True

    @property
    def full_name(self):
        return "{} {}".format(
            self.first_name,
            self.last_name,
        )

    def get_further_information(self):
        return self.further_information

    def get_person(self):
        return dict(
            full_name=self.full_name,
            further_information=self.further_information,
        )

    def __str__(self):
        return "Prénom : '{}', Nom : '{}', Further information : '{}'".format(
            self.first_name,
            self.last_name,
            self.further_information,
        )
