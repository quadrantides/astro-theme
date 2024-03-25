# -*- coding: utf-8 -*-
"""
Created on 2020, June 9th
@author: orion

"""
from astro.utils import str_date_for_filename

from aspects.models import Orb

from aspects.processes.base import Process
from aspects.processes.cycles import Cycle
from aspects.loggers import get_logger
from aspects.reports import execute


KNOWN_CYCLES = dict(

    sun_mercury=dict(
        planets=["sun", "mercury"],
        frequencies=['2D', '1D', '8H'],
    ),
    sun_venus=dict(
        planets=["sun", "venus"],
        frequencies=['4D', '2D', '8H'],
    ),
    sun_mars=dict(
        planets=["sun", "mars"],
        frequencies=['8D', '2D', '8H'],
    ),
    sun_jupiter=dict(
        planets=["sun", "jupiter"],
        frequencies=['8D', '2D', '8H'],
    ),
    sun_uranus=dict(
        planets=["sun", "uranus"],
        frequencies=['8D', '1D'],
    ),
    jupiter_saturn=dict(
        planets=["jupiter", "saturn"],
        frequencies=['8D', '2D', '8H'],
    ),
    jupiter_neptune = dict(
        planets=["jupiter", "neptune"],
        frequencies=['8D', '2D', '8H'],
    ),
)


class Loader(Process):

    def __init__(self, planet1, planet2, start, end, angles, orbs, visu_aspects_after_creation=False):
        super(Loader, self).__init__()

        self.cycle = None
        self.visu_aspects_after_creation = False

        self.init(planet1, planet2, start, end, angles, orbs, visu_aspects_after_creation=visu_aspects_after_creation)

    def init(self, planet1, planet2, start, end, angles, orbs, visu_aspects_after_creation=False):

        self.visu_aspects_after_creation = visu_aspects_after_creation
        self.set_logger(planet1, planet2, start, end)
        self.set_cycle(planet1, planet2, start, end, angles, orbs)

    def set_logger(self, planet1, planet2, start, end):
        str_start = str_date_for_filename(start)
        str_end = str_date_for_filename(end)
        logger_suffix = ".".join([planet1, planet2, str_start, str_end])
        # str_angles = "angles.{}".format(
        #     ".".join(["{:05}".format(angle) for angle in angles]),
        # )
        # str_orbs = "orbs.{}".format(
        #     ".".join([str(orb) for orb in orbs]),
        # )
        # logger_suffix = ".".join(
        #     [logger_suffix, str_angles, str_orbs],
        # )
        logger = get_logger(logger_suffix)
        self.add_logger(
            logger,
        )

    def get_cycle(self):
        return self.cycle

    def set_cycle(self, planet1, planet2, start, end, angles, orbs, logger=None):
        found = False
        key = None

        for key in KNOWN_CYCLES:
            planets = KNOWN_CYCLES[key]['planets']
            if planet1 in planets and planet2 in planets:
                found = True
                break

        if found and key:
            all_allowed_entries = Orb.objects.all()
            all_allowed_orbs = [entry.value for entry in all_allowed_entries]
            removed_orbs = []
            new_orbs = []
            for orb in orbs:
                if float(orb) not in all_allowed_orbs:
                    removed_orbs.append(orb)
                else:
                    new_orbs.append(orb)

            if len(removed_orbs):
                raise Exception(
                    "Les valeurs suivantes ne sont pas permises pour orbs : {}".format(
                        [str(orb) for orb in removed_orbs],
                    )
                )
            else:
                frequencies = KNOWN_CYCLES[key]['frequencies']
                time_range = [
                    start,
                    end,
                ]

                self.cycle = Cycle(
                    planet1,
                    planet2,
                    time_range,
                    angles,
                    new_orbs,
                    frequencies,
                    logger=self.get_logger(),
                )

        else:
            raise Exception(
                "La stratégie de recherche n'est pas connue pour le cycle demandé : {} - {}".format(
                    planet1,
                    planet2,
                )
            )

    def process(self, save=False):

        execute(self.cycle, save=save)
