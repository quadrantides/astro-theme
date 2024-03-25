# coding=utf-8
"""
Created on 2020, April 22th
@author: orion
"""
from transcend.processes import merge
from transcend.views.charts.theme.constants import WHEEL
from transcend.views.charts.theme.geometries.models import Model as BaseModel
from transcend.views.charts.theme.transform import get_layout_size


class Model(BaseModel):

    def __init__(self, chart):
        super(Model, self).__init__(chart)
        self.init()

    def init(self):
        self.load_chart()

    def load_chart(self):
        planets_bounds_in_polar_coords = self.get_planets_bounds_in_polar_coords()['radius']

        external_radius = WHEEL['houses']['annotations']['radius']['external']
        external_radius_in_xy_coords = external_radius / get_layout_size()

        chart = self.get_container()
        content = chart.get_content()

        structure = dict(
            opacity=0.5,
            visible=True,
            name="",
            annotation=dict(
                label="",
                x=0.0,
                y=0.0,
                radius=0.0,
                xanchor="center",
                yanchor="middle",
                font=dict(
                    color="#444",
                    size=11,
                ),
            ),
            line=dict(
                radius=dict(
                    min=0.0,
                    max=0.0,
                ),
                dash='dot',
                color="#444",
                width=1,
            ),
        )

        content = merge(
            structure,
            content,
        )

        content["annotation"]["radius"] = external_radius_in_xy_coords
        content["line"]["radius"]["min"] = planets_bounds_in_polar_coords["min"]
        content["line"]["radius"]["max"] = planets_bounds_in_polar_coords["max"]

    def get_data(self):
        return self.get_container()
