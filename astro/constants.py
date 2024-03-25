# coding=utf-8
"""
Created on 2019, Dec 17th
@author: orion
"""
import copy
import os
from bokeh.palettes import Category10, Greys3, Accent8

COLORS10 = Category10[10]

VERSION = "1.0"

DEBUG = False

PLANETS_POSITION_OUTPUTS = os.environ["PLANETS_POSITION_OUTPUTS"]

PLANETS_POSITION_OUTPUTS_HTML = os.path.join(
    PLANETS_POSITION_OUTPUTS,
    "HTML",
)

# APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# EPHEMERIS = os.path.join(
#     APP_ROOT,
#     "/DATA/swisseph",
# )

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

    'Ari', 'Tau', 'Gem', 'Cnc',
    'Leo', 'Vir', 'Lib', 'Sco',
    'Sgr', 'Cap', 'Aqr', 'Psc',
]

ZODIAC_NAMES = [

    'aries', 'taurus', 'gemini', 'cancer',
    'leo', 'virgo', 'libra', 'scorpio',
    'sagittarius', 'capricorn', 'aquarius', 'pisces',
]


ZODIAC_ELEMENTS = ['fire', 'earth', 'air', 'water'] * 3


ZODIAC_COLORS = [

    '#482900', '#6b3d00', '#5995e7', '#2b4972',
    '#c54100', '#2b286f', '#69acf1', '#ffd237',
    '#ff7200', '#863c00', '#4f0377', '#6cbfff',
]

TRANSCEND_REAL_PLANETS = [
    'sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn',
    'uranus', 'neptune', 'pluto',
]

QUADRANTIDES_BODIES = [
    'sun',
    'moon',
    'mercury',
    'venus',
    'mars',
    'jupiter',
    'saturn',
    'uranus',
    'neptune',
    'pluto',
    # 'true node',
    # 'osc. apogee',
    'chiron',
    # "Asc",
    # "Mc",
]

QUADRANTIDES_BODIES_COLORS = [
    "#FDE724",
    COLORS10[7],
    COLORS10[5],
    COLORS10[1],
    COLORS10[3],
    COLORS10[4],
    COLORS10[2],
    COLORS10[9],
    COLORS10[0],
    COLORS10[8],

    # Greys3[0],
    # Greys3[1],
    Accent8[5],

    # Accent8[0],
    # Accent8[2],
]

BODIES_COLORS = dict(
    sun="#FDE724",
    moon=COLORS10[7],
    mercury=COLORS10[5],
    venus=Accent8[5],
    mars=COLORS10[3],
    jupiter=COLORS10[4],
    saturn=COLORS10[2],
    uranus=COLORS10[9],
    neptune=COLORS10[0],
    pluto=COLORS10[8],
    chiron=COLORS10[1],
)

REAL_PLANETS = [
    'earth', 'chiron', 'pholus', 'ceres', 'pallas', 'juno', 'vesta',
]

PLANETS = REAL_PLANETS.copy()
PLANETS.extend(TRANSCEND_REAL_PLANETS)

TRANSCEND_POINTS_OF_INTEREST = [
    'Asc', 'Mc',
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
        'chiron',
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
