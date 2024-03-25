# coding=utf-8
"""
Created on 2020, April 27th
@author: orion
"""
from transcend.processes import merge
from transcend.views.charts.graphics.models import Model as GraphicsModel
from transcend.views.charts.theme.models import Model as BaseModel
from transcend.views.charts.theme.zodiac.constants import COLORS


class Model(BaseModel, GraphicsModel):

    def __init__(self, chart, dimensions=None):
        BaseModel.__init__(self, chart)
        GraphicsModel.__init__(self, dimensions=dimensions)
        self.init()

    def init(self):
        self.load_chart()

    def load_chart(self):

        chart = self.get_container()
        chart_name = chart.get_name()
        sub_chart_name = chart.get_sub_name()

        content = chart.get_content()

        colors = COLORS
        hovertext = chart_name
        if 'image' in content.keys():
            # => customized values
            textinfo = 'none'
        else:
            textinfo = 'label'

        rmax, rmin, domain = self.get_zodiac()

        images_radius_in_xy_coords = self.get_zodiac_annotation_radius()

        graduations = self.get_graduations()

        dtick = self.get_polar_angularaxis_dticks()

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
