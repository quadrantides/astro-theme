# coding=utf-8
"""
Created on 2020, April 8th
@author: orion
"""
import datetime
from django.utils.translation import ugettext as _


class OpenAstroInput(object):

    def __init__(

            self,
            identifier="",
            chart_name="",

    ):
        self.identifier = identifier
        self.chart_name = chart_name
        self.zodiactype = ""
        self.city = ''
        self.geolon = 0.0
        self.geolat = 0.0
        self.countrycode = ''
        self.timezonestr = ''

        self.postype = ""
        self.houses_system = ""
        self.chartview = ""
        self.date = datetime.datetime.now()
        self.transit_date = None
        self.altitude = 25
        self.sidereal_mode = ""

    def set_identifier(self, value):
        self.identifier = value

    def set_chart_name(self, value):
        self.chart_name = value

    def set_sidereal_mode(self, sidereal_mode):
        self.sidereal_mode = sidereal_mode

    def set_chartview(self, chartview):
        self.chartview = chartview

    def set_date(self, date):
        self.date = date

    def set_transit_date(self, date):
        self.transit_date = date

    def set_altitude(self, altitude):
        self.altitude = altitude

    def set_countrycode(self, countrycode):
        self.countrycode = countrycode

    def set_timezonestr(self, timezonestr):
        self.timezonestr = timezonestr

    def set_postype(self, postype):
        self.postype = postype

    def set_houses_system(self, houses_system):
        self.houses_system = houses_system

    def set_zodiactype(self, zodiactype):
        self.zodiactype = zodiactype

    def set_location(self, location):
        self.city = location

    def set_geolon(self, geolon):
        self.geolon = geolon

    def set_geolat(self, geolat):
        self.geolat = geolat

    def get_chart_name(self):
        return self.chart_name

    def get_transit_date(self):
        return self.transit_date

    def get_identifier(self):
        return self.identifier

    def get_data(self):
        return {
            "identifier": self.identifier,
            "chart_name": self.chart_name,
            "date": self.date,
            "transit_date": self.transit_date,
            "zodiactype": self.zodiactype,
            "location": self.city,
            "geolon": self.geolon,
            "geolat": self.geolat,
            "countrycode": self.countrycode,
            "timezonestr": self.timezonestr,
            "postype": self.postype,
            "houses_system": self.houses_system,
            "chartview": self.chartview,
            "altitude": self.altitude,
            'sidereal_mode': self.sidereal_mode,

        }


class Default(OpenAstroInput):
    def __init__(self, zodiactype, altitude=25):
        super(Default, self).__init__(chart_name=_("Anonymous"))
        self.zodiactype = zodiactype
        self.city = 'Paris'
        self.geolon = 2.3488
        self.geolat = 48.8534
        # self.city = 'Amiens'
        # self.geolon = 2.3
        # self.geolat = 49.9
        self.countrycode = 'FR'
        self.timezonestr = 'Europe/Paris'

        self.postype = "geo"
        self.houses_system = "P"
        self.chartview = "traditional"
        self.date = datetime.datetime.now()
        # self.date = datetime.datetime(2020, 6, 27, 14, 26)
        # self.date = datetime.datetime(2020, 6, 25, 14, 46)
        # self.date = datetime.datetime(2020, 6, 24, 10, 40)
        # self.date = datetime.datetime(1977, 12, 21, 9, 0)
        self.altitude = altitude


class TropicalDefault(Default):
    def __init__(self, houses_system="P"):
        super(TropicalDefault, self).__init__("tropical")
        self.houses_system = houses_system


class SiderealDefault(Default):
    def __init__(self, request=""):
        super(SiderealDefault, self).__init__("sidereal")
        self.siderealmode = "LAHIRI"

    def get_data(self):
        data = super(SiderealDefault, self).get_data()
        data.update(
            {"siderealmode": self.siderealmode}
        )
        return data
