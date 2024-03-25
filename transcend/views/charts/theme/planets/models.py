# coding=utf-8
"""
Created on 2020, April 13th
@author: orion
"""
from transcend.views.charts.theme.constants import WHEEL, THEME_ASPECTS_RADIUS, TRANSIT_ASPECTS_RADIUS

from transcend.views.charts.theme.models import Model as BaseModel


class Model(BaseModel):

    def __init__(self, chart):
        super(Model, self).__init__(chart)
        self.init()

    def init(self):
        self.load()

    def load(self):
        houses_rmin = THEME_ASPECTS_RADIUS
        if self.get_chart_name() == "transit":
            houses_rmin = TRANSIT_ASPECTS_RADIUS

        chart_definition = {

            'chart': {
                'planets': {
                    'chart': {
                        'theme': {
                            'radius': 0.0,
                        },
                        'transit': {
                            'radius': 0.0,
                        },
                    },
                    'box_size': 10,  # in degrees
                    "images": {
                        'sizex': 0.045,
                        'sizey': 0.045,
                        'opacity': 0.75,
                        'xanchor': "center",
                        'yanchor': "middle",
                    },
                },
            },
        }

        chart_definition['chart']['planets']['chart']['theme']['radius'] = \
            WHEEL['planets']['chart']['theme']['radius']
        chart_definition['chart']['planets']['chart']['transit']['radius'] = \
            WHEEL['planets']['chart']['transit']['radius']

        self.set_container(chart_definition)

    def get_data(self):
        return {
                'planets': self.get_container()
        }
