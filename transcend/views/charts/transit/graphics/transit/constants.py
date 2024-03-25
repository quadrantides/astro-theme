# coding=utf-8
"""
Created on 2020, August 25th
@author: orion

Calculation are given in cartesian coordinates

"""
VERSION = "1.0"

"""
    DIMENSIONS GEOMETRY
"""

GRADUATIONS_TICKLEN = 0

LAYOUT_WIDTH_PX = LAYOUT_WIDTH_PY = 680  # 720  # 1140 960 720 540

XAXIS_RANGE = YAXIS_RANGE = [-1, 1]


POLAR_DOMAIN_X = POLAR_DOMAIN_Y = [0.15, 0.85]
POLAR_DOMAIN_X = POLAR_DOMAIN_Y = [0.2, 0.8]
POLAR_DOMAIN_X = POLAR_DOMAIN_Y = [0.0, 1.0]

SCALE_FACTOR = 1 / (POLAR_DOMAIN_X[1] - POLAR_DOMAIN_X[0])

DIMENSIONS_WIDTH_PX = LAYOUT_WIDTH_PX
DIMENSIONS_HEIGHT_PX = DIMENSIONS_WIDTH_PX

POLAR_PLOT_RADIUS_PX = LAYOUT_WIDTH_PX * (POLAR_DOMAIN_X[1] - POLAR_DOMAIN_X[0])

"""
GRADUATIONS

    La structure de base du graphique est constituée, d'abord et avant tout, 
    du cercle trigonométrique (nommé graduations)

    A partir de cette structure, les éléments suivants peuvent être ajoutés:

      - les planètes,       (REQUIS)
      - le zodiac,          (OPTIONNEL)
      - les aspects         (OPTIONNEL)
"""

GRADUATIONS_RMIN = 0.75
GRADUATIONS_SIZE = 0.03
GRADUATIONS_RMAX = GRADUATIONS_RMIN + GRADUATIONS_SIZE

"""
    PLANETS
"""

PLANETS_RADIUS = GRADUATIONS_RMAX + 0.1
PLANETS_BOX_SIZE = 8
NB_PLANETS_BOXES = int(360 / PLANETS_BOX_SIZE)

"""
    HOUSES (OPTIONNEL)
"""
HOUSES_LINE_RMAX = 1.075
HOUSES_LINE_RMIN = GRADUATIONS_RMAX
HOUSES_ANNOTATION_RADIUS = HOUSES_LINE_RMAX - 0.075

"""
    ZODIAC (OPTIONNEL)
"""

ZODIAC_RMAX = GRADUATIONS_RMIN
ZODIAC_RMIN = ZODIAC_RMAX - 0.15

"""
    ASPECTS (OPTIONNEL)
"""
ASPECTS_RADIUS = ZODIAC_RMIN


DIMENSIONS = {
    'layout': dict(
        width=LAYOUT_WIDTH_PX,
        height=LAYOUT_WIDTH_PY,
        polar=dict(
            domain=dict(
                x=POLAR_DOMAIN_X,
                y=POLAR_DOMAIN_Y,
            ),
            angularaxis=dict(
                ticklen=GRADUATIONS_TICKLEN,
                dtick=1,
            ),
        ),
        xaxis=dict(
            range=XAXIS_RANGE,
        ),
        yaxis=dict(
            range=YAXIS_RANGE,
        ),
    ),
    'width': DIMENSIONS_WIDTH_PX,
    'height': DIMENSIONS_HEIGHT_PX,

    'color': {
        'tropical':  "#ff0066",
    },
    'title': {
        'position': {
            'top': {
                'left': {
                    'sorted_items': [
                        "transit identifier",
                        "theme identifier",
                        "date",
                        'location',
                        'latlon title',
                        'latlon value',
                        'houses_system',
                        'mode',
                    ],
                    "x0": -0.12,
                    "y0": 0.975,
                    "step": 0.03,
                },
                'right': {
                    "x0": 0.95,
                    "y0": 0.95,
                    "step": 0.03,
                },
            },
            'bottom': {
                'left': {
                    'sorted_items': [
                        'tropical title',
                        'tropical houses_system',
                    ],
                    "x0": -0.12,
                    "y0": 0.2,
                    "step": 0.03,
                },

                'right': {
                    'sorted_items': [
                        'sidereal title',
                        'sidereal houses_system',
                        'sidereal mode',
                    ],
                    "x0": 0.975,
                    "y0": 0.2,
                    "step": 0.03,
                },
            }

        },

    },
    'graduations': dict(
        radius=dict(
            internal=GRADUATIONS_RMIN,
            external=GRADUATIONS_RMAX,
        ),
    ),
    'zodiac': dict(
        radius=dict(
            internal=ZODIAC_RMIN,
            external=ZODIAC_RMAX,
        ),
    ),
    'houses': dict(
        annotations=dict(
            radius=HOUSES_ANNOTATION_RADIUS,
        ),
        lines=dict(
            radius=dict(
                internal=HOUSES_LINE_RMIN,
                external=HOUSES_LINE_RMAX,
            ),
        ),
    ),
    'planets': dict(
        radius=PLANETS_RADIUS,
        box_size=PLANETS_BOX_SIZE,
        line=dict(
            color='#000',
        ),
        image=dict(
            size=0.1,
        ),
    ),
    'points': dict(
        line=dict(
            color='#fac673',
        ),
    ),
    'aspects': dict(
        radius=ASPECTS_RADIUS,
    ),
}


def get_polar_width():
    scale = DIMENSIONS['layout']["polar"]["domain"]["x"][1]
    return scale * DIMENSIONS['layout']["width"]


def get_polar_width2():
    scale = DIMENSIONS['layout']["polar"]["domain"]["x"][1] - DIMENSIONS['layout']["polar"]["domain"]["x"][0]
    return scale * DIMENSIONS['layout']["width"]
