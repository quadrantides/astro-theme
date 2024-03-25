# coding=utf-8
"""
Created on 2019, Dec 20th
@author: orion
"""
import copy


CONSTELLATIONS_POSITIONS_ON_ECLIPTIC = dict(
    aries=dict(
        begin=dict(
            equatorial=dict(
                declination="10d0m0s",
                right_ascension="0h00m0s",
            ),
            longitude=0.0,
        ),
        end=dict(
            equatorial=dict(
                declination="18d0m0s",
                right_ascension="2h00m0s",
            ),
            longitude=30.0,
        ),
    ),
    taurus=dict(
        begin=dict(
            equatorial=dict(
                declination="18d0m0s",
                right_ascension="2h00m0s",
            ),
            longitude=30.0,
        ),
        end=dict(
            equatorial=dict(
                declination="23d0m0s",
                right_ascension="4h0m0s",
            ),
            longitude=60.0,
        ),
    ),
    gemini=dict(
        begin=dict(
            equatorial=dict(
                declination="23d0m0s",
                right_ascension="4h0m0s",
            ),
            longitude=60.0,
        ),
        end=dict(
            equatorial=dict(
                declination="21d0m0s",
                right_ascension="6h0m0s",
            ),
            longitude=90.0,
        ),
    ),
    cancer=dict(
        begin=dict(
            equatorial=dict(
                declination="21d0m0s",
                right_ascension="6h0m0s",
            ),
            longitude=90.0,
        ),
        end=dict(
            equatorial=dict(
                declination="15d0m0s",
                right_ascension="8h00m0s",
            ),
            longitude=120.0,
        ),
    ),
    leo=dict(
        begin=dict(
            equatorial=dict(
                declination="15d0m0s",
                right_ascension="8h00m0s",
            ),
            longitude=120.0,
        ),
        end=dict(
            equatorial=dict(
                declination="2d0m0s",
                right_ascension="10h00m0s",
            ),
            longitude=150.0,
        ),
    ),
    virgo=dict(
        begin=dict(
            equatorial=dict(
                declination="2d0m0s",
                right_ascension="10h00m0s",
            ),
            longitude=150.0,
        ),
        end=dict(
            equatorial=dict(
                declination="-13d0m0s",
                right_ascension="12h00m0s",
            ),
            longitude=180.0,
        ),
    ),
    libra=dict(
        begin=dict(
            equatorial=dict(
                declination="-13d0m0s",
                right_ascension="12h00m0s",
            ),
            longitude=180.0,
        ),
        end=dict(
            equatorial=dict(
                declination="-20d0m0s",
                right_ascension="14h0m0s",
            ),
            longitude=210.0,
        ),
    ),
    scorpio=dict(
        begin=dict(
            equatorial=dict(
                declination="-20d0m0s",
                right_ascension="14h0m0s",
            ),
            longitude=210.0,
        ),
        end=dict(
            equatorial=dict(
                declination="-21d0m0s",
                right_ascension="16h00m0s",
            ),
            longitude=240.0,
        ),
    ),
    sagittarius=dict(
        begin=dict(
            equatorial=dict(
                declination="-23d0m0s",
                right_ascension="16h00m0s",
            ),
            longitude=240.0,
        ),
        end=dict(
            equatorial=dict(
                declination="-20d0m0s",
                right_ascension="18h0m0s",
            ),
            longitude=270.0,
        ),
    ),
    capricorn=dict(
        begin=dict(
            equatorial=dict(
                declination="-20d0m0s",
                right_ascension="18h00m0s",
            ),
            longitude=270.0,
        ),
        end=dict(
            equatorial=dict(
                declination="-12d0m0s",
                right_ascension="20h0m0s",
            ),
            longitude=300.0,
        ),
    ),
    aquarius=dict(
        begin=dict(
            equatorial=dict(
                declination="-12d0m0s",
                right_ascension="20h0m0s",
            ),
            longitude=300.0,
        ),
        end=dict(
            equatorial=dict(
                declination="-3d0m0s",
                right_ascension="22h00m0.0s",
            ),
            longitude=330.0,
        ),
    ),
    pisces=dict(
        begin=dict(
            equatorial=dict(
                declination="-3d0m0s",
                right_ascension="22h00m0.0s",
            ),
            longitude=330.0,
        ),
        end=dict(
            equatorial=dict(
                declination="10d0m0s",
                right_ascension="0h00m0s",
            ),
            longitude=360.0,
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

