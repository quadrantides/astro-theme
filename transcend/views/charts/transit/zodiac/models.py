# coding=utf-8
"""
Created on 2020, August 13th
@author: orion
"""
from transcend.processes import merge
from transcend.views.charts.transit.constants import WHEEL
from transcend.views.charts.theme.geometries.models import Model as BaseModel


class Model(BaseModel):

    def __init__(self, chart):
        super(Model, self).__init__(chart)
        self.init()

    def init(self):
        self.load_chart()

    def load_chart(self):

        chart = self.get_container()
        chart_name = chart.get_name()
        sub_chart_name = chart.get_sub_name()

        content = chart.get_content()

        colors = WHEEL[chart_name]['zodiac']['pie']['colors']
        hovertext = chart_name
        textinfo = 'none'
        rmax, rmin, domain = self.get_zodiac_pie_bounds(WHEEL)

        donut_size_px = rmax - rmin

        images_radius_px = rmax - donut_size_px / 2.0

        images_radius_in_xy_coords = self.get_zodiac_pie_center_radius(WHEEL)

        graduations = self.get_planets_graduations(WHEEL)

        dtick = WHEEL["layout"]['polar']['angularaxis']['dtick']

        structure = dict(
            opacity=1.0,
            # opacity=0.5,
            visible=True,
            name=chart_name,
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
            image=dict(
                visible=False,
                radius=images_radius_in_xy_coords,
                sizex=0.05,
                sizey=0.05,
                xanchor="center",
                yanchor="middle",
                opacity=1.0,
                layer="above",
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
