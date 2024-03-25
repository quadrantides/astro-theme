# coding=utf-8
"""
Created on 2020, Jan 13th
@author: orion
"""
import pandas as pd
import datetime

from django.utils.translation import ugettext as _

import numpy as np

from transcend.processes import merge
from transcend.constants import DEBUG
from aspects.read.cycles import get as get_cycle
from aspects.read.aspects import get as get_all_aspects
from aspects.constants import get_default_orb

from transcend.openastro import openAstroInstance
from transcend.constants import is_planet_of_interest, is_point_of_interest
from transcend.constants import DATE_FORMAT


class Process(object):

    def __init__(
            self,
            selection,
    ):
        self.sidereal = dict()
        self.tropical = dict()
        self.planets = dict(
            tropical=dict(),
            sidereal=dict(),
        )
        self.transit_planets = dict(
            tropical=dict(),
            sidereal=dict(),
        )
        self.transit_aspects = dict(
            tropical=dict(),
            sidereal=dict(),
        )
        # self.asc = dict()
        # self.mc = dict()
        self.selection = None
        self.init(selection)

    def init(self, selection):
        self.selection = selection
        self.load()

    def load(self):
        self.load_sidereal()
        self.load_tropical()
        self.get_cycles()

    def load_sidereal(self):
        if 'sidereal' in self.selection.keys():
            openastro = openAstroInstance(
                self.selection['sidereal'].get_data()
            )
            self.sidereal = openastro.get_data()

    def get_tropical(self):
        return self.tropical

    def get_sidereal(self):
        return self.sidereal

    def load_tropical(self):
        if 'tropical' in self.selection.keys():
            openastro = openAstroInstance(
                self.selection['tropical'].get_data()
            )
            self.tropical = openastro.get_data()

    def extract(self, planets, method):
        data = dict()
        for key in planets.keys():
            if method(key):
                data[key] = planets[key]
        return data

    def set_planets(self):
        if "planets" in self.tropical.keys():
            self.planets['tropical'] = self.extract(
                    self.tropical["planets"],
                    is_planet_of_interest,
                )
        if "planets" in self.sidereal.keys():
            self.planets['sidereal'] = self.extract(
                    self.sidereal["planets"],
                    is_planet_of_interest,
                )

    def get_planets(self):
        if not self.planets['tropical'] and not self.planets['sidereal']:
            self.set_planets()

        return self.planets

    def get_planets_names(self):
        planets = self.get_planets()['tropical']
        if len(planets) == 0:
            planets = self.get_planets()['sidereal']
        return [key.capitalize() for key in planets.keys()]

    def has_transit_data(self, name):
        transit_planets = self.get_transit_planets()
        return True if len(transit_planets[name]) > 0 else False

    def set_transit_planets(self):
        if "transit" in self.tropical.keys():
            if self.tropical["transit"]["planets"]:
                self.transit_planets['tropical'] = self.extract(
                        self.tropical["transit"]["planets"],
                        is_planet_of_interest,
                    )
        if "transit" in self.sidereal.keys():
            if self.tropical["transit"]["planets"]:
                self.transit_planets['sidereal'] = self.extract(
                        self.sidereal["transit"]["planets"],
                        is_planet_of_interest,
                    )

    def get_transit_planets(self):
        if not self.transit_planets['tropical'] and not self.transit_planets['sidereal']:
            self.set_transit_planets()

        return self.transit_planets

    def get_transit_planets_names(self):
        planets = self.get_transit_planets()['tropical']
        if len(planets) == 0:
            planets = self.get_transit_planets()['sidereal']
        return [key.capitalize() for key in planets.keys()]

    def get_points(self):
        res = dict()
        if "planets" in self.tropical.keys():
            res.update(
                dict(
                    tropical=self.extract(
                        self.tropical["planets"],
                        is_point_of_interest,
                    ),
                ),
            )
        if "planets" in self.sidereal.keys():
            res.update(
                dict(
                    sidereal=self.extract(
                        self.sidereal["planets"],
                        is_point_of_interest,
                    ),
                ),
            )

        return res

    def get_tropical_selection(self):
        return self.tropical["selection"]

    def get_sidereal_selection(self):
        return self.sidereal["selection"]

    def get_tropical_settings(self):
        return self.tropical["settings"]

    def get_sidereal_settings(self):
        return self.sidereal["settings"]

    def extract_aspects(self, aspects):
        res = []
        for aspect in aspects:
            found = [False, False]
            for i, planet in enumerate(aspect['planets']):
                if is_planet_of_interest(planet['name']):
                    found[i] = True
            if found[0] and found[1]:
                res.append(aspect)
        return res

    def get_aspects(self):
        res = dict()
        if "aspects" in self.tropical.keys():
            res.update(
                dict(
                    tropical=self.extract_aspects(
                        self.tropical["aspects"],
                    ),
                ),
            )
        if "aspects" in self.sidereal.keys():
            res.update(
                dict(
                    sidereal=self.extract_aspects(
                        self.sidereal["aspects"],
                    ),
                ),
            )

        return res

    def get_transit_aspects(self):
        res = dict()
        if "transit" in self.tropical.keys():
            if "aspects" in self.tropical["transit"].keys():
                res.update(
                    dict(
                        tropical=self.extract_aspects(
                            self.tropical["transit"]["aspects"],
                        ),
                    ),
                )
        if "transit" in self.sidereal.keys():
            if "aspects" in self.sidereal["transit"].keys():
                res.update(
                    dict(
                        sidereal=self.extract_aspects(
                            self.sidereal["transit"]["aspects"],
                        ),
                    ),
                )

        return res

    def get_planets_aspects_and_points(self):
        return dict(
            planets=self.get_planets(),
            aspects=self.get_aspects(),
            points=self.get_points(),
        )

    def get_transit_planets_aspects_and_points(self):
        return dict(
            planets=self.get_transit_planets(),
            aspects=self.get_transit_aspects(),
            points=None,
        )

    def get_current_aspects(self):
        res = dict()
        if "aspects" in self.tropical.keys():
            res = self.extract_aspects(
                self.tropical["aspects"],
            )
        if "aspects" in self.sidereal.keys():
            res = self.extract_aspects(
                self.sidereal["aspects"],
            )

        return res

    def get_chart_name(self, zodiactype):
        return self.selection[zodiactype].get_chart_name()

    def get_theme_identifier(self, zodiactype):
        return self.selection[zodiactype].get_identifier()

    def get_transit_identifier(self, zodiactype):
        return self.selection[zodiactype].get_transit_date().strftime(DATE_FORMAT)

    def get_current_selection(self):
        if self.sidereal:
            res = self.sidereal["selection"]
        elif self.tropical:
            res = self.tropical["selection"]
        else:
            res = dict()
        return res

    def get_cycles(self):
        cycles = []
        selection = self.get_current_selection()
        str_date = selection["date"]
        start = datetime.datetime.strptime(str_date, DATE_FORMAT)
        dates = pd.date_range(
            start=start,
            periods=2,
            freq='100Y',
        ).to_pydatetime()
        end = dates[1]

        aspects = self.get_current_aspects()
        for aspect in aspects:
            planet1 = aspect['planets'][0]["name"]
            planet2 = aspect['planets'][1]["name"]
            rc, cycle = get_cycle(planet1, planet2)
            if rc.success:
                orb_value = get_default_orb(
                    aspect['aspect']['name'],
                )
                if orb_value > 0:
                    is_conjunction = aspect['aspect']['name'] == "conjunction"
                    if is_conjunction and cycle.is_internal:
                        conjunction_type = "superior" if aspect['aspect']['is_major'] else "inferior"
                    else:
                        conjunction_type = ""
                    rc, next_aspects = \
                        get_all_aspects(
                            planet1,
                            planet2,
                            aspect['aspect']['degree'],
                            start,
                            end,
                            orb_value=orb_value,
                            conjunction_type=conjunction_type,
                        )
                    if rc.success:
                        if len(next_aspects) > 0:
                            # if is_conjunction:
                            #     title = "{} {} {}, orb : {}".format(
                            #         _("List of"),
                            #         _(aspect['aspect']['name']),
                            #         _(conjunction_type),
                            #         orb_value,
                            #     )
                            # else:
                            #     title = "{} {}, orb : {}".format(
                            #         _("List of"),
                            #         _(aspect['aspect']['name']).capitalize(),
                            #         orb_value,
                            #     )
                            tab_name = "{}/{}".format(
                                    _(planet1).capitalize(),
                                    _(planet2).capitalize(),
                                )

                            cycles.append(
                                dict(
                                    tab_name=tab_name,
                                    is_internal=cycle.is_internal,
                                    aspect=dict(
                                        name=_(aspect['aspect']['name']),
                                        conjunction_type=_(conjunction_type),
                                        orb=orb_value,
                                        is_conjunction=is_conjunction,
                                        next=next_aspects,
                                    ),
                                ),
                            )

        return cycles
