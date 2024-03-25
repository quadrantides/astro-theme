# coding=utf-8
"""
Created on 2020, April 14th
@author: orion
"""
import numpy as np

from transcend.processes import merge
from transcend.models.points.structures import get_polar_point_structure

from transcend.models.planets.planets.clusters import Clusters
from transcend.views.processes import Process as BaseProcess

from transcend.views.constants import PLANET_ICONS, PLANET_ICONS_SIZE
# from transcend.constants import TRANSCEND_POINTS_OF_INTEREST
# from transcend.views.charts.theme.graphics.processes import get_display_order
from transcend.views.charts.theme.graphics.processes import get_segment_coordinates

from transcend.views.charts.models.planets.structures import get_planet_structure

from transcend.views.charts.theme.planets.planets.legend.processes import Process as LegendProcess

from transcend.views.charts.theme.graphics.images import get_one as get_graphic_image
from transcend.views.charts.theme.graphics.planets.planets.traces import get_polar_segment as get_polar_graphic_segment
from transcend.views.charts.theme.graphics.planets.planets.annotations import get as get_graphic_annotation
from transcend.views.charts.theme.graphics.planets.planets.traces import get_polar_marker as get_polar_graphic_marker


from transcend.views.charts.theme.figure.processes import get_coordinates

# GRADUATIONS

from transcend.views.charts.theme.graduations.processes import Process as GraduationsProcess
from transcend.views.charts.theme.planets.planets.graduations.models import Model as GraduationsModel

# ASPECTS

from transcend.views.charts.theme.planets.aspects.processes import Process as AspectsProcess
from transcend.views.charts.theme.planets.aspects.processes import get_planets_names as get_aspect_planets_names
from transcend.views.charts.theme.planets.aspects.models import Model as AspectsModel


# POINTS  OF INTEREST

from transcend.views.charts.theme.planets.points.processes import Process as PointsProcess
from transcend.views.charts.theme.planets.points.models import Model as PointsModel


# def get_planet(planet_names, label):
#
#     nb_refs = len(planet_names)
#     eod = False
#     found = False
#     i = 0
#     while not eod and not found:
#         if planet_names[i]["label"] == label:
#             found = True
#         if not found:
#             i += 1
#             if i > nb_refs - 1:
#                 eod = True
#
#     if found:
#         ref = planet_names[i]
#     else:
#         ref = None
#     return ref


def has_differences(planet, ref):
    has = abs(planet["angle"] - ref['angle']) >= 1
    return has


def convert_degrees_minutes(angle):
    degrees = int(angle)
    decimal = angle - degrees
    minutes = int(
        round(
            decimal * 60,
        ),
    )

    return "{}°{:02}'".format(
        degrees,
        minutes,
    )


def convert_degrees_minutes_seconds(angle):
    degrees = int(angle)
    decimal = angle - degrees
    minutes = int(
        decimal * 60,
    )
    reliquat = decimal * 60 - minutes
    seconds = int(
        round(
            reliquat * 60,
        )
    )

    return "{}°{:02}'{:02}''".format(
        degrees,
        minutes,
        seconds,
    )


def get_text_position(angle):
    yanchor = "middle"
    xanchor = "center"

    if 0 < angle <= 5:
        yanchor = "top"
        xanchor = "center"
    elif 354 < angle <= 359:
        yanchor = "bottom"
        xanchor = "center"
    elif 180 <= angle <= 182:
        yanchor = "bottom"
        xanchor = "center"
    elif 183 <= angle <= 185:
        yanchor = "top"
        xanchor = "center"
    # if angle <= 15 or angle > 315:
    #     yanchor = "top"
    #     xanchor = "right"
    # elif 15 < angle <= 135:
    #     xanchor = "right"
    #     yanchor = "bottom"
    # elif 175 < angle <= 185:
    #     yanchor = "top"
    #     xanchor = "right"
    # elif 135 < angle <= 225:
    #     yanchor = "bottom"
    #     xanchor = "right"
    # elif 225 < angle <= 315:
    #     yanchor = "bottom"
    #     xanchor = "right"

    textposition = '{} {}'.format(xanchor, yanchor)

    return dict(
        textposition=textposition,
        xanchor=xanchor,
        yanchor=yanchor,
    )
    # {'textposition': textposition, "xanchor": }


def find_order(positions, label):
    orders = list(positions.keys())
    nb_orders = len(orders)
    eod = nb_orders == 0
    found = False
    i = 0
    order = -1
    while not eod and not found:
        orderi = orders[i]
        if positions[orderi]["label"] == label:
            found = True
        if not found:
            i += 1
            if i > nb_orders - 1:
                eod = True

        else:
            order = orderi

    return order


def get_new_positions(point, positions, box_size):
    point_label = point['label']
    point_angle = point['angle']
    point_order = find_order(positions, point_label)

    if point_order > -1:
        position_point_angle = positions[point_order]['angle']
        if point_angle != position_point_angle:
            translation = point_angle - position_point_angle
            previous_position_angle = positions[point_order]['angle']
            positions[point_order]['angle'] = positions[point_order]['angle'] + translation

            eod = point_order == 0
            found = False
            while not eod and not found:
                point_order -= 1
                diff = previous_position_angle + translation - positions[point_order]['angle']
                if diff < 0:
                    # translation = positions[point_order]['angle'] - previous_position_angle + translation
                    previous_position_angle = positions[point_order]['angle']
                    positions[point_order]['angle'] += translation
                    eod = point_order == 0
                elif diff <= box_size:
                    previous_position_angle = positions[point_order]['angle']
                    translation = diff - box_size
                    positions[point_order]['angle'] += translation
                    eod = point_order == 0
                else:
                    break

    return positions


class Process(BaseProcess):

    def __init__(
            self,
            data_model,
            chart,
            view_model=None,
            load_only=False,
            show_aspects=True,
            show_points=True,
            show_annotations=True,
            graphics_dimensions=None,
    ):
        super(Process, self).__init__(
            data_model,
            chart,
            view_model,
        )
        self.graphics_dimensions = graphics_dimensions
        self.legend = None
        self.show_aspects = show_aspects
        self.show_points = show_points
        self.show_annotations = show_annotations
        self.processes = dict(
            graduations=None,
            aspects=None,
            points=None,
        )
        self.process(load_only=load_only)

    def get_source(self, key):
        if key not in PLANET_ICONS.keys():
            key = 'unknown'
        return PLANET_ICONS[key]

    def get_image_size(self, key):
        if key not in PLANET_ICONS_SIZE.keys():
            key = 'unknown'
        return PLANET_ICONS_SIZE[key] * 0.9

    # def get_display_order(self, box_size, planets):
    #
    #     angles = []
    #
    #     for planet in planets:
    #         angles.append(
    #             planet['angle']
    #         )
    #
    #     return get_display_order(box_size, angles)

    def add_legend(self, planets):
        self.legend = LegendProcess(
            planets,
        )

    # def get_values(self, planets, orders, box_size):
    #
    #     selected = "#C54C82"
    #     unselected = "#fff"
    #
    #     values = []
    #     colors = []
    #     labels = []
    #     angles = []
    #     planets_position = {}
    #
    #     for i in range(len(orders)):
    #         order = orders[i]
    #         planet = planets[order]
    #
    #         if i == 0:
    #             box_center = planet['angle']
    #         else:
    #
    #             # we add unselectable area between two planets if necessary
    #
    #             dist = planet['angle'] - angle_ref
    #
    #             nb_box_sizes = int(dist / box_size)
    #
    #             if nb_box_sizes > 0:
    #                 # exclusive inside box
    #                 unselectable_interval_size = nb_box_sizes * box_size
    #             elif dist - box_size / 2.0 > 0:
    #                 unselectable_interval_size = dist - box_size / 2.0
    #             else:
    #                 unselectable_interval_size = 0.0
    #
    #             if unselectable_interval_size:
    #
    #                 box_center_candidate = box_center + unselectable_interval_size + box_size
    #                 if box_center_candidate - planet['angle'] <= unselectable_interval_size:
    #                     unselectable_interval_size -= box_center_candidate - planet['angle']
    #                 values.append(unselectable_interval_size)
    #                 colors.append(unselected)
    #                 labels.append("")
    #
    #             box_center += unselectable_interval_size + box_size
    #
    #         # we add the current planet selectable area
    #
    #         values.append(box_size)
    #         colors.append(selected)
    #         planet_label = planet['label']
    #         labels.append(
    #             planet_label,
    #         )
    #         angles.append(
    #             box_center,
    #         )
    #
    #         if i == 0:
    #             angle_ref = angles[-1] + (box_size / 2.0)
    #         else:
    #             angle_ref += unselectable_interval_size + box_size
    #
    #         planets_position[order] = dict(
    #             label=planet_label,
    #             angle=box_center,
    #         )
    #
    #     reliquat = 360 - sum(values)
    #
    #     if reliquat > 0:
    #         values.append(reliquat)
    #         colors.append(unselected)
    #         labels.append("")
    #
    #     rotation = - values[0] + box_size / 2 + 90 - angles[0]
    #     return rotation, values, colors, labels, planets_position

    def load_graduations(self):
        self.processes['graduations'] = self.get_planets_graduations(
            GraduationsProcess,
            GraduationsModel,
            load_only=True,
            graphics_dimensions=self.graphics_dimensions,
        )

    def load_aspects(self):
        self.processes['aspects'] = self.get_aspects(
            AspectsProcess,
            AspectsModel,
            load_only=True,
        )

    def load_points(self):
        self.processes['points'] = self.get_points(
            PointsProcess,
            PointsModel,
        )

    def get_planets_structure(self, model):

        zodiactype = self.get_zodiactype()

        view_data = self.view_model.get_data().get_content()
        box_size = view_data['box_size']

        planets = model.get_data()
        orders = model.get_display_order(box_size)
        clusters = Clusters(model, box_size)
        graphical_positions, planet_orb = clusters.get_graphical_positions()

        planets_structure = []

        for i in range(len(orders)):
            order = orders[i]
            planet = planets[order]

            planet_structure = get_planet_structure()

            planet_structure = merge(
                view_data,
                planet_structure,
            )

            planet_structure = merge(
                planet,
                planet_structure,
            )

            planet_label = planet_structure['label']

            radius_scale = 0.5 if planet_label != "asc" and planet_label != "mc" else 0.0

            # if planet_label == "Asc" or planet_label == "Mc":
            #     continue
            planet_structure['name'] = planet_label

            # # for tests only
            # if zodiactype == "tropical":
            #     planet_structure['angle'] = i * 10

            # if planet_label not in legend_planets:
            #     legend_planets.append(planet_label)

            angle = planet_structure['angle']

            elongation_degrees, angle_degree_minutes, elongation_degree_minutes_seconds, zodiac_label = \
                self.get_elongation(angle)

            # new angle calculation if no enough place to display de image in front of angle graduation

            # angle_on_chart = angle
            # if len(processed_angles) > 0:
            #     dangle = angle - processed_angles[-1]
            #     if dangle < box_size:
            #         angle_on_chart = processed_angles[-1] + box_size

            # planet_structure['angle_on_chart'] = angle_on_chart

            external_radius = planet_structure['line']['points']['external']['radius']
            internal_radius = planet_structure['line']['points']['internal']['radius']
            dr = radius_scale * (external_radius - internal_radius)

            # image ADDING

            try:
                planet_structure['image']['angle'] = graphical_positions[planet_label]
            except KeyError:
                continue
            source = self.get_source(planet_label)
            planet_structure['image']['source'] = source
            planet_structure['image']['name'] = planet_label.capitalize()
            planet_structure['image']['label'] = planet_structure['image']['name']

            planet_structure['image']['sizex'] = self.get_image_size(planet_label) * planet_orb/box_size
            planet_structure['image']['sizey'] = self.get_image_size(planet_label) * planet_orb/box_size

            coordinates = get_coordinates(
                planet_structure['image']['angle'],
                planet_structure['image']['radius'] - dr,
            )

            planet_structure['image'] = merge(
                coordinates,
                planet_structure['image'],
            )

            if self.show_annotations:
                # annotation adding
                planet_structure['annotation']['opacity'] = planet_structure['opacity']
                planet_structure['annotation']['visible'] = planet_structure['visible']
                planet_structure['annotation']['name'] = planet_structure['name']

                # planet_structure['annotation']['text'] = "<b>{}</b>".format(
                #     angle_degree_minutes,
                # )
                planet_structure['annotation']['text'] = angle_degree_minutes

                coordinates = get_coordinates(
                    graphical_positions[planet_label],
                    planet_structure['annotation']['radius'] - dr,
                )

                planet_structure['annotation'] = merge(
                    coordinates,
                    planet_structure['annotation'],
                )

                planet_structure['annotation'] = merge(

                    get_text_position(
                        graphical_positions[planet_label],
                    ),
                    planet_structure['annotation'],
                )

            # line adding

            # internal point

            planet_structure['line']['points']['internal']['angle'] = angle
            planet_structure['line']['points']['external']['angle'] = graphical_positions[planet_label]
            planet_structure['line']['points']['external']['radius'] -= dr
            planet_structure['line']['points']['internal'] = merge(
                coordinates,
                planet_structure['line']['points']['internal'],
            )

            planet_structure['line']['opacity'] = planet_structure['opacity']
            planet_structure['line']['visible'] = planet_structure['visible']
            planet_structure['line']['name'] = planet_structure['name']

            # if planet_label == "Asc" or planet_label == "Mc":
            #     planet_structure['line']['color'] = WHEEL["points"]['line']['color']
            #     planet_structure['line']['width'] = 3

            # pie adding

            angle_degree_minutes_seconds = convert_degrees_minutes_seconds(angle)

            planet_structure['marker']['visible'] = planet_structure['visible']
            planet_structure['marker']['name'] = planet_structure['name']

            planet_structure['marker']['customdata'] = [
                [
                    "planet-{}-{}".format(
                        zodiactype,
                        planet_structure['marker']['name'],
                    ),
                    zodiactype.capitalize(),
                    elongation_degree_minutes_seconds,
                    zodiac_label.capitalize(),
                    angle_degree_minutes_seconds,
                ],
            ]

            planet_structure['marker']['name'] = planet_structure['image']['name']
            planet_structure['marker']['text'] = [
                planet_label.capitalize(),
            ]

            planet_structure['marker']['angle'] = planet_structure['image']['angle']

            planets_structure.append(
                planet_structure
            )

        return planets_structure

    def load(self):

        # graduations loading

        self.load_graduations()

        if self.show_aspects:

            # aspects loading

            self.load_aspects()

        # point loading

        if self.show_points:
            self.load_points()

        # planets loading

        zodiactype = self.get_zodiactype()

        # db data model loading

        data = self.get_chart().get_content()

        theme_planets_model = self.get_container().get_planets(zodiactype)

        planets_structure = self.get_planets_structure(theme_planets_model)

        data['planets'] = planets_structure

        # transit_planets_model = self.get_container().get_transit_planets(zodiactype)
        #
        # transit_planets = \
        #     transit_planets_model.get_data()
        #
        # if len(transit_planets) > 0:
        #
        #     planets_structure = self.get_planets_structure(transit_planets_model)
        #
        #     data['planets'] = planets_structure

        # View model adding

    def get_elongation(self, angle):
        zodiac_angles = self.get_zodiac()['angles']
        zodiac_labels = self.get_zodiac()['labels']

        zodiac_angles = np.array(zodiac_angles) % 360
        zodiac_labels = np.array(zodiac_labels)

        sorted_indices = np.argsort(zodiac_angles)

        angles = zodiac_angles[sorted_indices]
        dangles = angle - angles
        positive = dangles >= 0

        if len(dangles[positive]) == 0:
            dangles = angle + 360 - angles
            positive = dangles >= 0

        elongation_index = np.argmin(dangles[positive])
        elongation = dangles[positive][elongation_index]
        zodiac_label = zodiac_labels[sorted_indices[positive][elongation_index]]
        label_degree_minutes_seconds = convert_degrees_minutes_seconds(elongation)
        angle_degree_minutes = convert_degrees_minutes(elongation)

        label_degrees = "{}°".format(
            int(
                round(elongation),
            ),
        )

        return label_degrees, angle_degree_minutes, label_degree_minutes_seconds, zodiac_label

    def get_data(self):
        return merge(
            self.legend.get_data(),
            self.get_chart().get_content(),
        )

    def get_planet(self, label):
        refs = self.get_chart().get_content()['planets']

        nb_refs = len(refs)
        eod = False
        found = False
        i = 0
        while not eod and not found:
            if refs[i]["label"] == label:
                found = True
            if not found:
                i += 1
                if i > nb_refs - 1:
                    eod = True

        if found:
            ref = refs[i]
        else:
            ref = None
        return ref

    def create_planet_graphics_components(self, planet):

        self.add_traces(
            [
                get_polar_graphic_segment(
                    planet['line'],
                ),
                get_polar_graphic_marker(
                    planet['marker'],
                ),
            ]
        )
        annotation = get_graphic_annotation(
            planet['annotation'],
        )
        self.add_annotations([annotation])

        image = get_graphic_image(planet['image'])
        self.add_images([image])

    def is_concerned_by_conjunction(self, planet_name):

        res = False
        if self.processes["aspects"]:

            # conjunction migration to planet level

            aspects = self.processes["aspects"].get_conjunctions()

            nb_conjunctions = len(aspects)

            if nb_conjunctions:
                eod = False
                found = False
                i = 0
                while not eod and not found:
                    aspect = aspects[i]
                    aspect_planet_names = [
                        aspect['line']['points']['planet1']['label'].lower(),
                        aspect['line']['points']['planet2']['label'].lower(),
                    ]
                    if planet_name in aspect_planet_names:
                        found = True
                    else:
                        i += 1
                        if i > nb_conjunctions - 1:
                            eod = True

                res = found

        return res

    # def create_conjunctions_graphics_components(self, data=None):
    #
    #     if self.processes["aspects"]:
    #         conjunctions = self.processes["aspects"].get_container().get_conjunctions()
    #         print('ok')

    def create_planets_graphics_components(self, data=None):

        # if self.processes["aspects"]:
        #     clusters = self.processes["aspects"].get_container().get_conjunctions()
        #     print('ok')

        for planet in self.get_chart().get_content()['planets']:
            # if self.is_concerned_by_conjunction(planet["name"]):
            #     planet['image']['sizex'] *= 0.5
            #     planet['image']['sizey'] *= 0.5
            #     planet['annotation']['font']['size'] = 8

            self.create_planet_graphics_components(
                planet,
            )

    def search_for_related_conjunctions(self, angles):
        """
            Recherche et fusion des conjonctions connexes
        """
        new_angles = angles.copy()

        nb_angles = len(angles)
        add = []
        remove = []
        for i, anglei in enumerate(angles[0:-1]):
            j = i + 1
            eod = j > nb_angles - 1
            union = False
            while not union and not eod:
                anglej = angles[j]
                mask = np.isin(anglei, anglej)
                if len(anglei[mask]) == 1:
                    common_anglej = anglei[mask][0]
                    condition1 = common_anglej == anglei[-1] and common_anglej == anglej[0]
                    condition2 = common_anglej == anglei[0] and common_anglej == anglej[-1]
                    if condition1 or condition2:
                        """
                        Deux conjonctions connexes trouvées => fusion en une seule
                        """
                        if condition1:
                            add.append(
                                np.concatenate(
                                    [anglei, anglej[1::]],
                                ),
                            )
                        if condition2:
                            add.append(
                                np.concatenate(
                                    [anglej, anglei[1::]],
                                ),
                            )
                        remove.extend([i, j])
                        union = True

                j += 1
                eod = j > nb_angles - 1

            if union:
                for index in sorted(remove, reverse=True):
                    new_angles.pop(index)
                for angle in add:
                    new_angles.append(angle)

        return new_angles

    def get_conjunctions(self, angles, all_aspect_planets_names):

        new_angles = []
        indexes_to_hide = []
        view_data = self.view_model.get_data().get_content()
        box_size = view_data['box_size']

        nb_angles = len(angles)
        indexes = list(range(nb_angles))

        elongations = []
        lengths = []
        for anglesi in angles:
            amin = int(min(anglesi))
            amax = int(max(anglesi))
            if not len(range(amin, amax)) % box_size == 0:
                amax = amax + 360 if amax < amin else amax
            elongations.append(
                np.array(range(amin, amax+1)),
            )
            lengths.append(
                amax - amin,
            )

        sindexes = np.argsort(lengths)
        selongations = np.array(elongations)[sindexes]
        nb_elongations = nb_angles

        for i, elongationi in enumerate(selongations[0:-1]):
            j = i + 1
            eod = j > nb_elongations - 1
            is_contained = False
            while not is_contained and not eod:
                elongationj = selongations[j]
                mask = np.isin(elongationi, elongationj)
                is_contained = len(elongationi[mask]) == len(elongationi)
                j += 1
                eod = j > nb_elongations - 1

            if is_contained:
                indexes_to_hide.append(
                    indexes[sindexes[i]],
                )
            else:
                new_angles.append(elongationi)

        new_angles.append(selongations[-1])

        # union des conjonctions qui sont connexes, le cas échéant

        nb_new_angles = len(new_angles)

        j = i + 1
        eod = j > nb_elongations - 1
        previous_nb_new_angles = nb_new_angles
        search_for_related_conjunctions = True
        while search_for_related_conjunctions:
            new_angles = self.search_for_related_conjunctions(new_angles)
            nb_new_anglesi = len(new_angles)
            if nb_new_anglesi == previous_nb_new_angles:
                search_for_related_conjunctions = False
            else:
                previous_nb_new_angles = nb_new_anglesi

        return new_angles

    def update_conjunction_aspects_position(self, orb=10):

        if self.processes["aspects"]:

            # conjunction migration to planet level

            aspects = self.processes["aspects"].get_conjunctions()
            if len(aspects) > 0:
                planet_structure = get_planet_structure()
                view_data = self.view_model.get_data().get_content()
                planet_structure = merge(
                    view_data,
                    planet_structure,
                )
                all_angles = []
                all_aspect_planets_names = []
                for aspect in aspects:
                    aspect_planets_names = get_aspect_planets_names(aspect)
                    all_aspect_planets_names.append(aspect_planets_names)
                    planets_angles = []
                    planets_radius = []
                    radii_min = []
                    radii_max = []
                    planets_points = []
                    for planet_name in aspect_planets_names:
                        planet = self.get_planet(planet_name)
                        # if not planet:
                        #     # Asc and Mc
                        #     planet = self.get_planet(planet_name.capitalize())
                        if planet:
                            point = get_polar_point_structure()
                            point['radius'] = planet['image']['radius']
                            point['angle'] = planet['image']['angle']
                            planets_points.append(
                                point,
                            )
                            planets_angles.append(
                                planet['line']['points']['external']['angle'],
                            )
                            planets_radius.append(
                                planet['line']['points']['external']['radius'] - 0.02,
                            )
                            radii_min.append(planet['line']['points']['internal']['radius'])
                            radii_max.append(planet['line']['points']['external']['radius'])
                        else:
                            print('ko')
                    if len(planets_points) == 2:
                        if abs(planets_angles[0] - planets_angles[1]) > 2 * orb:
                            print('stop')
                            planets_angles[np.argmin(planets_angles)] += 360
                        all_angles.append(
                            planets_angles,
                        )
                        aspect["marker"]["visible"] = False
                        # coordinates = dict(
                        #     radius=[
                        #         radii_min[0],
                        #         radii_min[1],
                        #         radii_min[1] + (radii_max[1] - radii_min[1]) / 2,
                        #         radii_min[0] + (radii_max[0] - radii_min[0]) / 2,
                        #     ],
                        #     angle=[
                        #         planets_angles[0],
                        #         planets_angles[1],
                        #         planets_angles[1],
                        #         planets_angles[0],
                        #     ],
                        # )
                        # aspect['marker'] = merge(
                        #     coordinates,
                        #     aspect['marker'],
                        # )

                        # aspect['marker']['customdata'] = [aspect['marker']['customdata']] * nb_points

                conjunctions = self.get_conjunctions(all_angles, all_aspect_planets_names)
                internal_radius = planet_structure['line']['points']['internal']['radius']
                external_radius = planet_structure['line']['points']['external']['radius']
                dr = 0.5 * (external_radius - internal_radius)
                radii = [
                    planet_structure['line']['points']['external']['radius'] - dr + 0.0025,
                    planet_structure['line']['points']['external']['radius'] - dr + 0.02,
                ]
                for aspect in aspects:
                    self.processes["aspects"].remove(aspect)
                for conjunction in conjunctions:
                    angles = [conjunction[0], conjunction[-1]]
                    self.processes["aspects"].set_conjunction(radii, angles)

    def create_aspects_graphics_components(self, data=None):

        if self.processes["aspects"]:

            self.processes["aspects"].create_graphics_components()
            components = self.processes["aspects"].get_graphics_components()

            self.add(components)

    def create_points_graphics_components(self, data=None):

        if self.processes["points"]:
            self.processes["points"].create_graphics_components()
            components = self.processes["points"].get_graphics_components()

            self.add(components)

    def create_graduations_graphics_components(self, data=None):
        if self.processes["graduations"]:

            self.processes["graduations"].create_graphics_components()
            components = self.processes["graduations"].get_graphics_components()
            self.add(components)

    def create_graphics_components(self, data=None):

        self.create_points_graphics_components(data=data)
        self.create_graduations_graphics_components(data=data)

        self.create_planets_graphics_components(data=data)
        self.update_conjunction_aspects_position()
        self.create_aspects_graphics_components(data=data)
