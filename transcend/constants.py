# coding=utf-8
"""
Created on 2019, Dec 17th
@author: orion
"""
import copy
import os
from django.utils.translation import ugettext_lazy as _

VERSION = "1.0"

DEBUG = False

# APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# EPHEMERIS = os.path.join(
#     APP_ROOT,
#     "/DATA/swisseph",
# )

ANGLE_OFFSET = 180

DATE_FORMAT = "%Y-%m-%d %H:%M"

# APP_DATA = '/home/patrice/opt/openastro.org-data-1.9'
APP_DATA = "/home/patrice/PycharmProjects/astrology/transcend/DATA"

EPHEMERIS = os.path.join(
    APP_DATA,
    "swisseph",
)

ASTROLIB_DB = os.path.join(
    APP_DATA,
    "db",
    "astrolib.sql",
)

GEONAMES_DB = os.path.join(
    APP_DATA,
    "db",
    "geonames.sql",
)

ZODIAC_CODES = [

    _('Ari'), _('Tau'), _('Gem'), _('Cnc'),
    _('Leo'), _('Vir'), _('Lib'), _('Sco'),
    _('Sgr'), _('Cap'), _('Aqr'), _('Psc'),
]

ZODIAC_NAMES = [

    _('aries'), _('taurus'), _('gemini'), _('cancer'),
    _('leo'), _('virgo'), _('libra'), _('scorpio'),
    _('sagittarius'), _('capricorn'), _('aquarius'), _('pisces'),
]

ZODIAC = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius',
          'capricorn', 'aquarius', 'pisces']

ZODIAC_ELEMENTS = [_('fire'), _('earth'), _('air'), _('water')] * 3


ZODIAC_COLORS = [

    '#482900', '#6b3d00', '#5995e7', '#2b4972',
    '#c54100', '#2b286f', '#69acf1', '#ffd237',
    '#ff7200', '#863c00', '#4f0377', '#6cbfff',
]

TRANSCEND_REAL_PLANETS = [
    'sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn',
    'uranus', 'neptune', 'pluto',
]

REAL_PLANETS = [
    'earth', 'chiron', 'pholus', 'ceres', 'pallas', 'juno', 'vesta',
]

TRANS_TRANSCEND_REAL_PLANETS = [
    _('sun'), _('moon'), _('mercury'), _('venus'), _('mars'), _('jupiter'), _('saturn'),
    _('uranus'), _('neptune'), _('pluto'),
]

TRANS_REAL_PLANETS = [
    _('earth'), _('chiron'), _('pholus'), _('ceres'), _('pallas'), _('juno'), _('vesta'),
]

PLANETS = REAL_PLANETS.copy()
PLANETS.extend(TRANSCEND_REAL_PLANETS)

TRANSCEND_POINTS_OF_INTEREST = [
    'asc', 'mc',
]

OTHER_POINTS_OF_INTEREST = [
    'mean node', 'true node', 'mean apogee', 'osc. apogee',
    'intp. apogee', 'intp. perigee', 'day pars',
    'night pars', 'south node', 'marriage pars', 'black sun', 'vulcanus', 'persephone',
    'true lilith',
]

POINTS_OF_INTEREST = copy.copy(TRANSCEND_POINTS_OF_INTEREST)
POINTS_OF_INTEREST.extend(OTHER_POINTS_OF_INTEREST)

PLANETS_OF_INTEREST = copy.copy(TRANSCEND_REAL_PLANETS)
PLANETS_OF_INTEREST.extend(
    [
        'true node',
        'true lilith',
        'chiron'
    ],
)
PLANETS_OF_INTEREST.extend(
    copy.copy(TRANSCEND_POINTS_OF_INTEREST),
)


def is_point_of_interest(name):
    return name in TRANSCEND_POINTS_OF_INTEREST


def is_planet_of_interest(name):
    return name in PLANETS_OF_INTEREST


DEFAULT_ALTITUDE = 0

DATA_TYPES = [
    "Combine",
    "Solar",
    "SecondaryProgression",
    "Transit",
    "Composite",
]

HOUSES_SYSTEM = {
    "P": "Placidus",
    "K": "Koch",
    "O": "Porphyrius",
    "R": "Regiomontanus",
    "C": "Campanus",
    "A": "Equal (Cusp 1 = Asc)",
    "V": "Vehlow Equal (Asc = 1/2 House 1)",
    "W": "Whole",
    "X": "Axial Rotation",
    "H": "Azimuthal or Horizontal System",
    "T": "Polich/Page ('topocentric system')",
    "B": "Alcabitus",
    "G": "Gauquelin sectors",
    "M": "Morinus"
}

CHART_VIEW_TYPES = [
    "traditional",
    "european",
]

ZODIAC_TYPES = ["sidereal", "tropical"]

SIDEREAL_MODES = [

    "FAGAN_BRADLEY",
    "LAHIRI",
    "DELUCE",
    "RAMAN",
    "USHASHASHI",
    "KRISHNAMURTI",
    "DJWHAL_KHUL",
    "YUKTESHWAR",
    "JN_BHASIN",
    "BABYL_KUGLER1",
    "BABYL_KUGLER2",
    "BABYL_KUGLER3",
    "BABYL_HUBER",
    "BABYL_ETPSC",
    "ALDEBARAN_15TAU",
    "HIPPARCHOS",
    "SASSANIAN",
    "J2000",
    "J1900",
    "B1950",
]
