# coding=utf-8
"""
Created on 2020, May 7th
@author: orion
"""
from transcend.processes import merge
from transcend.views.charts.graphics.constants import DIMENSIONS
from transcend.views.charts.theme.compounded.geometries.models import Model as BaseModel


class Model(BaseModel):

    def __init__(self, chart):
        super(Model, self).__init__(chart, sub_chart_name="sidereal")
        self.init()

    def init(self):
        self.load_chart()

    def load_chart(self):

        chart = self.get_container()
        chart_name = chart.get_name()

        zodiactype = "tropical"
        content = chart.get_content()

        colors = DIMENSIONS[chart_name][zodiactype]['zodiac']['pie']['colors']
        hovertext = zodiactype
        textinfo = 'none'

        rmax, rmin, domain = self.get_zodiac_pie_bounds_sidereal()

        graduations = self.get_planets_graduations()

        dtick = DIMENSIONS["layout"]['polar']['angularaxis']['dtick']

        structure = dict(
            opacity=1.0,
            # opacity=0.5,
            visible=True,
            name=zodiactype,
            pie=dict(
                domain=domain,
                colors=colors,
                hole=rmin,
                textinfo=textinfo,
                hoverinfo="label+text",
                # hovertext=hovertext,
                # hoverinfo='label+text',
                hovertemplate="" +
                "%{label}<br>" +
                "<i>%{customdata[0]}</i>",
                marker=dict(
                    line=dict(
                        width=1.0,
                        color="#444",
                    ),
                ),

            ),
            segment=dict(
                ticks=dict(
                    dtick=dtick,
                ),
                points=dict(
                    internal=dict(
                        radius=graduations["radius"]['min'],
                    ),
                    external=dict(
                        radius=graduations["radius"]['max'],
                    ),
                ),
                line=dict(
                    dash='solid',
                    color="#444",
                    width=1,
                ),
            ),
        )

        merge(
            structure,
            content,
        )

    def get_data(self):
        return self.get_container()
