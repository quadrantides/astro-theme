# coding=utf-8
"""
Created on 2020, December 20th
@author: orion
"""
from astro.zodiac.astronomical.processes import Process
from astro.zodiac.astronomical.constants import get_constellations_names


if __name__ == '__main__':

    process = Process()
    data = process.get_data()
    for name in get_constellations_names():
        print(
            "{} longitude begin  {} end {}".format(
                name,
                round(data[name]["begin"]["longitude"]),
                round(data[name]["end"]["longitude"]),
            ),
        )
