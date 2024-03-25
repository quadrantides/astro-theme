# coding=utf-8
"""
Created on 2019, Dec 20th
@author: orion
"""
import copy


VERNAL_POINT_POSITION = dict(
    equatorial=dict(
        declination=0.0,
        right_ascension=0.0,
    ),
    longitude=0.0,
)

CONSTELLATIONS_NAMES_ON_ECLIPTIC = [

    'aries', 'taurus', 'gemini', 'cancer',
    'leo', 'virgo', 'libra', 'scorpio',
    'sagittarius', 'capricorn', 'aquarius', 'pisces',
]

CONSTELLATIONS_POSITIONS_ON_ECLIPTIC = dict(
    aries=dict(
        begin=dict(
            equatorial=dict(
                declination="10d0m0s",
                right_ascension="1h45m0s",
            ),
            longitude=28.0,
        ),
        end=dict(
            equatorial=dict(
                declination="18d0m0s",
                right_ascension="3h20m0s",
            ),
            longitude=52.0,
        ),
    ),
    taurus=dict(
        begin=dict(
            equatorial=dict(
                declination="18d0m0s",
                right_ascension="3h20m0s",
            ),
            longitude=52.0,
        ),
        end=dict(
            equatorial=dict(
                declination="23d0m0s",
                right_ascension="6h0m0s",
            ),
            longitude=90.0,
        ),
    ),
    gemini=dict(
        begin=dict(
            equatorial=dict(
                declination="23d0m0s",
                right_ascension="6h0m0s",
            ),
            longitude=90.0,
        ),
        end=dict(
            equatorial=dict(
                declination="21d0m0s",
                right_ascension="8h0m0s",
            ),
            longitude=118.0,
        ),
    ),
    cancer=dict(
        begin=dict(
            equatorial=dict(
                declination="21d0m0s",
                right_ascension="8h0m0s",
            ),
            longitude=118.0,
        ),
        end=dict(
            equatorial=dict(
                declination="15d0m0s",
                right_ascension="9h20m0s",
            ),
            longitude=138.0,
        ),
    ),
    leo=dict(
        begin=dict(
            equatorial=dict(
                declination="15d0m0s",
                right_ascension="9h20m0s",
            ),
            longitude=138.0,
        ),
        end=dict(
            equatorial=dict(
                declination="2d0m0s",
                right_ascension="11h40m0s",
            ),
            longitude=175.0,
        ),
    ),
    virgo=dict(
        begin=dict(
            equatorial=dict(
                declination="2d0m0s",
                right_ascension="11h40m0s",
            ),
            longitude=175.0,
        ),
        end=dict(
            equatorial=dict(
                declination="-13d0m0s",
                right_ascension="14h20m0s",
            ),
            longitude=217.0,
        ),
    ),
    libra=dict(
        begin=dict(
            equatorial=dict(
                declination="-13d0m0s",
                right_ascension="14h20m0s",
            ),
            longitude=217.0,
        ),
        end=dict(
            equatorial=dict(
                declination="-20d0m0s",
                right_ascension="16h0m0s",
            ),
            longitude=242.0,
        ),
    ),
    scorpio=dict(
        begin=dict(
            equatorial=dict(
                declination="-20d0m0s",
                right_ascension="16h0m0s",
            ),
            longitude=242.0,
        ),
        end=dict(
            equatorial=dict(
                declination="-21d0m0s",
                right_ascension="16h20m0s",
            ),
            longitude=247.0,
        ),
    ),
    ophiucus=dict(
        begin=dict(
            equatorial=dict(
                declination="-21d0m0s",
                right_ascension="16h20m0s",
            ),
            longitude=247.0,
        ),
        end=dict(
            equatorial=dict(
                declination="-23d0m0s",
                right_ascension="17h40m0s",
            ),
            longitude=265.0,
        ),
    ),
    sagittarius=dict(
        begin=dict(
            equatorial=dict(
                declination="-23d0m0s",
                right_ascension="17h40m0s",
            ),
            longitude=265.0,
        ),
        end=dict(
            equatorial=dict(
                declination="-20d0m0s",
                right_ascension="20h10m0s",
            ),
            longitude=300.0,
        ),
    ),
    capricorn=dict(
        begin=dict(
            equatorial=dict(
                declination="-20d0m0s",
                right_ascension="20h10m0s",
            ),
            longitude=300.0,
        ),
        end=dict(
            equatorial=dict(
                declination="-12d0m0s",
                right_ascension="22h0m0s",
            ),
            longitude=328.0,
        ),
    ),
    aquarius=dict(
        begin=dict(
            equatorial=dict(
                declination="-12d0m0s",
                right_ascension="22h0m0s",
            ),
            longitude=328.0,
        ),
        end=dict(
            equatorial=dict(
                declination="-3d0m0s",
                right_ascension="23h30m0.0s",
            ),
            longitude=352.0,
        ),
    ),
    pisces=dict(
        begin=dict(
            equatorial=dict(
                declination="-3d0m0s",
                right_ascension="23h30m0.0s",
            ),
            longitude=352.0,
        ),
        end=dict(
            equatorial=dict(
                declination="10d0m0s",
                right_ascension="1h45m0s",
            ),
            longitude=28.0,
        ),
    ),
)


def get_constellations_names():
    return CONSTELLATIONS_POSITIONS_ON_ECLIPTIC.keys()


def get_positions():
    positions = copy.deepcopy(CONSTELLATIONS_POSITIONS_ON_ECLIPTIC)
    return positions


def get_data():
    data = dict()
    for name in CONSTELLATIONS_POSITIONS_ON_ECLIPTIC.keys():
        data[name] = dict(
            begin=dict(
                longitude=CONSTELLATIONS_POSITIONS_ON_ECLIPTIC[name]["begin"]["longitude"],
            ),
            end=dict(
                longitude=CONSTELLATIONS_POSITIONS_ON_ECLIPTIC[name]["end"]["longitude"],
            ),
        )
    return data
