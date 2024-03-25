# coding=utf-8
"""
Created on 2020, December 6th
@author: orion
"""
import numpy as np

from transcend.processes import merge

from transcend.constants import ANGLE_OFFSET

from transcend.views.processes import Process as BaseProcess

from transcend.views.constants import PLANET_ICONS

from transcend.views.charts.models.retrogrades.structures import get_retrograde_structure
# from transcend.views.charts.theme.planets.planets.legend.processes import Process as LegendProcess

from transcend.views.charts.ephemeris.graphics.retrogrades.retrogrades.traces import \
    get_polar_segment as get_polar_graphic_segment

from transcend.views.charts.ephemeris.graphics.retrogrades.retrogrades.annotations import \
    get as get_graphic_annotation


from transcend.views.charts.theme.figure.processes import get_coordinates

# GRADUATIONS

from transcend.views.charts.theme.graduations.processes import Process as GraduationsProcess
from transcend.views.charts.ephemeris.retrogrades.retrogrades.graduations.models import Model as GraduationsModel

# REVOLUTIONS

from transcend.views.charts.ephemeris.retrogrades.revolutions.charts import \
    get_process_chart as get_revolutions_process_chart
from transcend.views.charts.ephemeris.retrogrades.revolutions.charts import \
    get_view_chart as get_revolutions_view_chart

from transcend.views.charts.ephemeris.retrogrades.revolutions.processes import Process as RevolutionsProcess
from transcend.views.charts.ephemeris.retrogrades.revolutions.models import Model as RevolutionsModel

DATE_FORMAT = "%d %B %Y"
DECIMAL_PRECISION = 2


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
        xanchor = "right"
    elif 354 < angle <= 359:
        yanchor = "bottom"
        xanchor = "center"
        xanchor = "right"
    elif 180 <= angle <= 182:
        yanchor = "bottom"
        xanchor = "center"
        xanchor = "left"
    elif 183 <= angle <= 185:
        yanchor = "top"
        xanchor = "center"
        xanchor = "left"
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
        self.show_annotations = show_annotations
        self.processes = dict(
            graduations=None,
            revolutions=None,
        )
        self.process(load_only=load_only)

    def get_source(self, key):
        if key not in PLANET_ICONS.keys():
            key = 'unknown'
        return PLANET_ICONS[key]

    def load_revolutions(self):

        theme = self.get_chart().get_theme()
        chart_name = self.get_chart_name()
        sub_chart_name = self.get_sub_chart_name()

        process = RevolutionsProcess(
            self.get_container(),
            get_revolutions_process_chart(
                theme,
                chart_name,
                sub_chart_name=sub_chart_name,
            ),
            RevolutionsModel(
                get_revolutions_view_chart(
                    theme,
                    chart_name,
                    sub_chart_name=sub_chart_name,
                ),
                dimensions=self.graphics_dimensions,
            ),
            load_only=True,
        )
        self.processes['revolutions'] = process

    # def add_legend(self, planets):
    #     self.legend = LegendProcess(
    #         planets,
    #     )

    def load_graduations(self):
        self.processes['graduations'] = self.get_planets_graduations(
            GraduationsProcess,
            GraduationsModel,
            load_only=True,
            graphics_dimensions=self.graphics_dimensions,
        )

    def get_retrogrades_structure(self, model):

        view_data = self.view_model.get_data().get_content()

        retrogrades = model.get_data()["chart"]["retrogrades"]

        r_spiral, theta_spiral = self.processes['revolutions'].get_spiral_coordinates(model)

        retrogrades_structure = []

        for retrograde in retrogrades:

            retrograde_structure = get_retrograde_structure()

            retrograde_structure = merge(
                view_data,
                retrograde_structure,
            )

            retrograde_structure = merge(
                retrograde,
                retrograde_structure,
            )

            # annotation adding
            # retrograde_structure['annotation']['opacity'] = retrograde_structure['opacity']
            # retrograde_structure['annotation']['visible'] = retrograde_structure['visible']
            # retrograde_structure['annotation']['name'] = retrograde_structure['name']

            theta_0 = ANGLE_OFFSET + retrograde["end"]["longitude"]
            theta_1 = ANGLE_OFFSET + retrograde["begin"]["longitude"]

            indexes = np.where((theta_spiral >= theta_0) & (theta_spiral <= theta_1))[0]

            theta = theta_spiral[indexes]
            r = r_spiral[indexes]

            delta_date = retrograde["end"]["date"] - retrograde["begin"]["date"]
            central_year = (retrograde["begin"]["date"] + delta_date / 2.0).year
            # retrograde_structure['annotation']['text'] = central_year
            #
            # central_angle = theta[0] + (theta[-1] - theta[0]) / 2.0
            #
            # central_r = r[0] + (r[-1] - r[0]) / 2.0
            #
            # coordinates = get_coordinates(
            #     central_angle,
            #     central_r + 0.07,
            # )
            #
            # retrograde_structure['annotation'] = merge(
            #     coordinates,
            #     retrograde_structure['annotation'],
            # )
            #
            # retrograde_structure['annotation'] = merge(
            #
            #     get_text_position(
            #         central_angle,
            #     ),
            #     retrograde_structure['annotation'],
            # )

            # line adding

            retrograde_structure['line']["theta"] = theta
            retrograde_structure['line']["r"] = r

            retrograde_structure['line']['opacity'] = retrograde_structure['opacity']
            retrograde_structure['line']['visible'] = retrograde_structure['visible']

            retrograde_nb_days = (retrograde['end']['date'] - retrograde['begin']['date']).days

            if retrograde["end"]["date"].year == retrograde["begin"]["date"].year:
                line_text = retrograde["begin"]["date"].year
            else:
                line_text = "{} / {}".format(
                    retrograde["begin"]["date"].year,
                    retrograde["end"]["date"].year,
                )

            begin = "Begin   {:15} {:15} {}".format(
                retrograde['begin']['date'].strftime(format=DATE_FORMAT),

                retrograde['begin']['zodiac'],
                "{:05.2f}°".format(
                    round(
                        retrograde['begin']['longitude_in_zodiac'],
                        DECIMAL_PRECISION,
                    )
                )
            )
            end = "End     {:15} {:15} {}".format(
                retrograde['end']['date'].strftime(format=DATE_FORMAT),
                retrograde['end']['zodiac'],
                "{:05.2f}°".format(
                    round(
                        retrograde['end']['longitude_in_zodiac'],
                        DECIMAL_PRECISION,
                    )
                )
            )
            retrograde_structure['line']['custom_data'] = [
                [
                    "Period : {} days".format(
                        retrograde_nb_days,
                    ),
                    begin,
                    end,
                ]
            ]

            retrograde_structure['line']['text'] = line_text

            desc = [
                "{}".format(central_year),
                str(retrograde_nb_days),
                retrograde['begin']['date'].strftime(format=DATE_FORMAT),

                retrograde['begin']['zodiac'],
                "{}°".format(
                    round(
                        retrograde['begin']['longitude_in_zodiac'],
                        DECIMAL_PRECISION,
                    )
                ),

                retrograde['end']['date'].strftime(format=DATE_FORMAT),
                retrograde['end']['zodiac'],
                "{}°".format(
                    round(
                        retrograde['end']['longitude_in_zodiac'],
                        DECIMAL_PRECISION,
                    )
                ),

            ]

            retrograde_structure['line']['name'] = ", ".join(
                desc,
            )

            retrogrades_structure.append(
                retrograde_structure
            )

        return retrogrades_structure

    def load(self):

        # revolutions loading

        self.load_revolutions()

        # graduations loading

        self.load_graduations()

        data = self.get_chart().get_content()

        model = self.get_container()

        retrogrades_structure = self.get_retrogrades_structure(model)

        data['retrogrades'] = retrogrades_structure

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

    def create_retrograde_graphics_components(self, retrograde):

        self.add_traces(
            [
                get_polar_graphic_segment(
                    retrograde['line'],
                ),
            ]
        )

        # annotation = get_graphic_annotation(
        #     retrograde['annotation'],
        # )
        # self.add_annotations([annotation])

    def create_retrogrades_graphics_components(self, data=None):

        for retrograde in self.get_chart().get_content()['retrogrades']:
            self.create_retrograde_graphics_components(
                retrograde,
            )

    def create_revolutions_graphics_components(self, data=None):
        if self.processes["revolutions"]:
            self.processes["revolutions"].create_graphics_components()
            components = self.processes["revolutions"].get_graphics_components()
            self.add(components)

    def create_graduations_graphics_components(self, data=None):
        if self.processes["graduations"]:

            self.processes["graduations"].create_graphics_components()
            components = self.processes["graduations"].get_graphics_components()
            self.add(components)

    def create_graphics_components(self, data=None):

        self.create_graduations_graphics_components(data=data)
        # self.create_revolutions_graphics_components(data=data)
        self.create_retrogrades_graphics_components(data=data)
