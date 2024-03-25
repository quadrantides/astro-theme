# coding=utf-8
"""
Created on 2020, August 16th
@author: orion
"""
from transcend.processes import merge
from transcend.views.charts.transit.constants import WHEEL
from transcend.views.charts.theme.geometries.models import Model as BaseModel
from transcend.views.charts.theme.geometries.models import get_domain


class Model(BaseModel):

    def __init__(self, chart):
        super(Model, self).__init__(chart)
        self.init()

    def init(self):
        self.load_chart()

    def get_houses_pie_min_radius(self, wheel):
        chart_name = self.get_chart_name()
        chart_theme = self.get_theme()

        return wheel[chart_name]['houses'][chart_theme]['radius']['min']

    def get_houses_pie_max_radius(self, wheel):
        chart_name = self.get_chart_name()
        chart_theme = self.get_theme()

        return wheel[chart_name]['houses'][chart_theme]['radius']['max']

    def get_planets_graduations(self, wheel):
        chart_theme = self.get_theme()
        if chart_theme == "transit":
            rmax, rmin, domain = self.get_zodiac_pie_bounds(wheel)

            internal_radius = rmax * (domain['x'][1] - domain['x'][0])
            external_radius = internal_radius + WHEEL["graduations"][chart_theme]["circle"]["size"]
        elif chart_theme == "theme":
            internal_radius = WHEEL["graduations"][chart_theme]["rmin"]
            external_radius = internal_radius + WHEEL["graduations"][chart_theme]["circle"]["size"]

        return dict(
            radius=dict(
                min=internal_radius,
                max=external_radius,
            )
        )

    def get_houses_lines_bounds(self, wheel):

        internal_radius = self.get_planets_graduations(wheel)['radius']['max']
        external_radius = self.get_houses_pie_max_radius(wheel)

        return dict(
            radius=dict(
                min=internal_radius,
                max=external_radius,
            )
        )

    def load_chart(self):

        chart = self.get_container()
        chart_name = chart.get_name()
        chart_theme = self.get_theme()
        colors = WHEEL[chart_name]['houses'][chart_theme]['colors']

        lines_houses_bounds = self.get_houses_lines_bounds(WHEEL)

        rmax, rmin, domain = self.get_houses_pie_bounds(WHEEL)

        content = chart.get_content()

        structure = dict(
            opacity=0.75,
            visible=True,
            name="",
            line=dict(
                opacity=0.4,
                points=dict(
                    internal=dict(
                        radius=lines_houses_bounds["radius"]['min'],
                    ),
                    external=dict(
                        radius=lines_houses_bounds["radius"]['max'],
                    ),
                ),
                dash='solid',
                color="#000",
                width=1.5,
            ),
            annotation=dict(
                label="",
                x=0.0,
                y=0.0,
                radius=lines_houses_bounds["radius"]['max'],
                xanchor="center",
                yanchor="middle",
                font=dict(
                    color="#000",
                    size=12,
                ),
            ),
            pie=dict(
                domain=domain,
                hole=rmin,
                colors=colors,
                # textinfo='none',
                textinfo='label',
                hovertext='',
                # hovertext=' ',
                # hoverinfo='none',
                marker=dict(
                    line=dict(
                        width=1.0,
                        color="#888",
                    ),
                ),
                hoverinfo='label',
                hovertemplate="" +
                "%{label}<br>" +
                "<i>%{customdata[0]}</i>",
            ),
        )

        merge(
            structure,
            content,
        )

    def get_data(self):
        return self.get_container()
