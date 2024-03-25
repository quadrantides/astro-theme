# coding=utf-8
"""
Created on 2020, June 5th
@author: orion
"""
import pandas as pd

from astro.planets.positions.from_swiss_ephemeris import get_data as get_swe_data

from aspects.models import Planet
from aspects.models import Orb
from aspects.models import Cycle2
from aspects.models import get_cycle_name
from aspects.models import get_aspect_model
from aspects.models import get_conjunction_model
from aspects.models import get_coverage_model
from aspects.models import validate_angle

from aspects.visualizations import aspects as create_aspects_visualization

from .manager import AspectsManager
from .base import Process
from .coverages import exists as coverage_exists


PRECISION = 0.001

DATE_FORMAT = "%Y-%m-%d %H:%M"


class Cycle(Process):

    def __init__(
            self,
            planet1,
            planet2,
            time_range,
            angles,
            orbs,
            frequencies,
            frequency=None,
            events=None,
            logger=None,
    ):
        super(Cycle, self).__init__(logger=logger)
        self.planet1 = planet1.lower()
        self.planet2 = planet2.lower()
        self.time_range = time_range
        self.angles = angles
        self.frequency = frequency
        self.events = events
        self.orbs = orbs
        self.frequencies = frequencies
        self.process_orbs = True
        self.cycles = []

        self.manager = AspectsManager(
            self.angles,
        )

    def exists(self):
        cycle_name = get_cycle_name(self.planet1, self.planet2)
        res = False
        coverage_model = get_coverage_model(cycle_name)
        for angle in self.angles:
            for orb in self.orbs:
                if coverage_exists(coverage_model, self.planet1, self.planet2, angle, orb, self.time_range):
                    res = True
                    break
        return res

    def set_process_orbs(self, value):
        self.process_orbs = value

    def get_orbs(self):
        if self.process_orbs:
            return self.orbs
        else:
            return [self.orbs[0]]

    def process(self, frequency_index, process_orbs=True):

        self.set_process_orbs(process_orbs)

        if frequency_index == 0:
            self.set_aspects(
                self.get_dates(self.frequencies[frequency_index]),
                just_one_aspect=False,
            )

            self.manager.set_nb_aspects_expected()

            self.get_logger().info(
                "FIN DE LA RECHERCHE des aspects à la fréquence de {}".format(
                    self.frequencies[frequency_index],
                ),
            )
            self.get_logger().info(
                "   {} ASPECT(S) TROUVÉS".format(
                    len(self.manager.get_container()),
                ),
            )

            print(
                "Recherche n° {} : {} aspect(s) trouvé(s)".format(
                    frequency_index + 1,
                    len(self.manager.get_container()),
                ),
            )

        elif len(self.manager.get_container()) > 0:
            processes = self.manager.get_container()
            self.manager.reinit()
            for process in processes:
                aspect = process.get_container()
                # on élargit l'intervalle pour trouver l'aspect avec une plus grande précision
                # new start date
                start = aspect.get_start()
                dates = pd.date_range(
                    end=start,
                    periods=2,
                    freq=self.frequencies[frequency_index-1],
                ).to_pydatetime()

                new_start = dates[0]
                # new end date
                end = aspect.get_end()
                dates = pd.date_range(
                    start=end,
                    periods=2,
                    freq=self.frequencies[frequency_index-1],
                ).to_pydatetime()

                new_end = dates[1]

                new_dates = self.get_dates(
                    self.frequencies[frequency_index],
                    start=new_start,
                    end=new_end,
                ).tolist()

                self.set_aspects(
                    new_dates,
                    just_one_aspect=False,
                )

        for aspect in self.manager.get_container():
            print(aspect.get_container())

    def calculate(self, visualize=False):
        nb_frequencies = len(self.frequencies)
        for frequency_index in range(nb_frequencies):
            process_orbs = frequency_index == nb_frequencies - 1
            self.process(frequency_index=frequency_index, process_orbs=process_orbs)
        if visualize:
            self.visualize()

    def calculate_if_not_exists(self):
        if not self.exists():
            self.calculate(visualize=True)
        self.save()

    def get_dates(self, freq, start=None, end=None):
        if not start:
            start = self.time_range[0]
        if not end:
            end = self.time_range[1]
        dates = pd.date_range(start=start, end=end, freq=freq)
        return dates.to_pydatetime()

    def set_aspects(self, dates, just_one_aspect=False):

        swe_data = get_swe_data(dates, self.planet1, self.planet2)

        planets_longitudes = swe_data.get_longitudes()
        planets_latitudes = swe_data.get_latitudes()
        planets_distances = swe_data.get_distances()

        planets = planets_longitudes.columns.to_list()

        planet1_index = planets.index(self.planet1)
        planet2_index = planets.index(self.planet2)

        planet1_latitudes = planets_latitudes[planets[planet1_index]].to_list()
        planet2_latitudes = planets_latitudes[planets[planet2_index]].to_list()

        planet1_longitudes = planets_longitudes[planets[planet1_index]].to_list()
        planet2_longitudes = planets_longitudes[planets[planet2_index]].to_list()

        # self.manager.set_angles(
        #     planets_latitudes[planets[planet1_index]]-planets_latitudes[planets[planet2_index]],
        # )

        self.manager.set_orbs(
            self.get_orbs(),
        )
        self.manager.set_just_one_aspect(just_one_aspect)

        nb_records = len(dates)
        eod = False
        i = 0

        while not eod:

            ra1 = planet1_longitudes[i]
            ra2 = planet2_longitudes[i]

            latitude1 = planet1_latitudes[i]
            latitude2 = planet2_latitudes[i]

            # initialization

            # angular_distance = abs(ra1 - ra2)
            angular_distance = ra2 - ra1
            # angular_distance = angular_distance % 360

            right_ascension = ra2 - (ra2 - ra1) / 2.0
            # right_ascension = right_ascension % 360

            # on cherche à savoir s'il y a un nouvel aspect en à traiter

            aspects = self.manager.get_loading_in_progress_aspects(angular_distance)

            # print(
            #     "Date = {} - angular distance = {} - ra = {} (ra1 : {}, ra2 : {}) ".format(
            #         dates[i],
            #         angular_distance,
            #         right_ascension,
            #         ra1,
            #         ra2,
            #     ),
            # )
            for aspect in aspects:
                if aspect.is_conjunction():
                    if self.planet1 == "sun":
                        latitude_distance = abs(latitude2 - latitude1)

                        sun_index = planet1_index
                        sun_distances = planets_distances[planets[sun_index]].to_list()
                        other_planet_distances = planets_distances[planets[planet2_index]].to_list()

                        sun_distance = sun_distances[i]
                        planet_distance = other_planet_distances[i]

                        aspect.update(
                            dates[i],
                            angular_distance,
                            right_ascension,
                            latitude_distance,
                            sun_distance,
                            planet_distance,
                        )
                else:
                    aspect.update(
                        dates[i],
                    )
                # print(aspect.get_container())

            if self.manager.stop():
                break

            # date suivante

            i += 1
            if i > nb_records - 1:
                eod = True
        if eod:
            self.manager.created_all_aspects_in_progress()

    def get_aspects(self):
        return self.manager.get_container()

    def visualize(self):

        freq = self.frequencies[-1]

        start = self.time_range[0]
        end = self.time_range[1]

        new_dates = pd.date_range(
            start=start,
            end=end,
            freq=freq,
        ).to_pydatetime()

        swe_data = get_swe_data(new_dates, self.planet1, self.planet2)

        planets_longitudes = swe_data.get_longitudes()
        planets = planets_longitudes.columns.to_list()

        planet1_index = planets.index(self.planet1)
        planet2_index = planets.index(self.planet2)

        planet1_longitudes = planets_longitudes[planets[planet1_index]].to_list()
        planet2_longitudes = planets_longitudes[planets[planet2_index]].to_list()

        create_aspects_visualization(
            new_dates,
            [planet1_longitudes, planet2_longitudes],
            self.planet1,
            self.planet2,
            aspects=self.get_aspects(),
        )

    def save(self):

        planet1 = Planet.objects.get(name=self.planet1)
        planet2 = Planet.objects.get(name=self.planet2)

        cycle = Cycle2.objects.get(planet1=planet1.id, planet2=planet2.id)

        cycle_name = cycle.get_name()

        aspect_model = get_aspect_model(cycle_name)
        conjunction_model = get_conjunction_model(cycle_name)
        coverage_model = get_coverage_model(cycle_name)

        aspects = self.get_aspects()

        if len(aspects) > 0:

            # if visu_aspects_after_creation:
            #
            #     if len(self.frequencies) > 1:
            #         freq = self.frequencies[-2].to_pydatetime()
            #     else:
            #         freq = self.frequencies[0]
            #     dates = pd.date_range(
            #         start=self.time_range[0],
            #         end=self.time_range[1],
            #         freq=freq,
            #     )
            #
            #     create_aspects_visualization(dates, self.planet1, self.planet2, aspects=aspects)

            for aspect in aspects:

                angle = validate_angle(
                    aspect.get_angle()
                )
                if angle < 0:
                    angle += 360

                orb_instance = Orb.objects.get(value=aspect.get_orb())

                # CREATION ou MISE A JOUR de l'aspect dans la table ASPECTS

                aspect_instance, created = aspect_model.objects.update_or_create(
                    cycle=cycle,
                    angle=angle,
                    orb=orb_instance,
                    start=aspect.get_start(),
                    end=aspect.get_end(),
                )

                if created:

                    if planet2.name in ["mercury", "venus"] and aspect.is_conjunction():

                        # CREATION ou MISE A JOUR de l'aspect dans la table CONJUNCTIONS

                        conjunction_instance, created = conjunction_model.objects.update_or_create(
                            aspect=aspect_instance,
                            type=aspect.get_type(),
                            true=aspect.get_true(),
                        )

                    coverage_instance, created = coverage_model.objects.update_or_create(
                        cycle=cycle,
                        angle=angle,
                        orb=orb_instance,
                        start=self.time_range[0],
                        end=self.time_range[1],
                    )

                else:

                    prefix = "MISE A JOUR"
                    self.get_logger().info(
                        "Table {}_{} / {} de l'enregistrement : {}".format(
                            cycle_name.upper(),
                            "ASPECTS",
                            prefix,
                            str(aspect_instance),
                        )
                    )

        # CREATION  de la recherche dans la table COVERAGES

        # for angle in self.angles:
        #
        #     for orb in self.orbs:
        #
        #         orb_instance = Orb.objects.get(value=orb)
        #
        #         coverage_instance, created = coverage_model.objects.update_or_create(
        #             cycle=cycle,
        #             angle=angle,
        #             orb=orb_instance,
        #             start=self.time_range[0],
        #             end=self.time_range[1],
        #         )
                # prefix = "CREATION" if created else "MISE A JOUR"
                # self.get_logger().info(
                #     "Table {}_{} / {} de l'enregistrement : {}".format(
                #         cycle_name.upper(),
                #         "COVERAGES",
                #         prefix,
                #         str(coverage_instance),
                #     )
                # )

    # def test_event(self, event):
    #     half_hours = 48
    #     begin_date = event.get_date() - datetime.timedelta(hours=half_hours)
    #     dates = [begin_date + datetime.timedelta(hours=hours) for hours in range(2 * half_hours)]
    #     events = self.set_aspects(
    #         dates,
    #         event.get_angle(),
    #         type=event.conjunction_type(),
    #         true=event.is_true_conjunction(),
    #     )
    #     if not events:
    #         raise Exception(
    #             "L'événement spécifié : {} n'a pas été trouvé (à +∕- 2 jours) pour le cycle {}-{}"
    #             "Veuillez fournir un évenement réel".format(
    #                 event,
    #                 self.planet1,
    #                 self.planet2,
    #             ),
    #         )
    #
    # def test_events(self):
    #     if self.events:
    #         for event in self.events:
    #             self.test_event(event)
    #
    #     pass
