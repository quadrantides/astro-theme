# coding=utf-8
"""
Created on 2020, April 17th
@author: orion
"""
from transcend.views.charts.theme.models import Model as BaseModel


class Model(BaseModel):

    def __init__(self):
        super(Model, self).__init__("")
        self.init()

    def init(self):
        self.load()

    def load(self):

        chart_definition = {

            'chart': {
                'planet': {
                    'legend': {
                        'visible': True,
                        "image": {
                            'radius': 0.78,
                            'sizex': 0.05,
                            'sizey': 0.05,
                            'opacity': 0.65,
                            # 'rmargin': 0.1,
                            'xanchor': "center",
                            'yanchor': "middle",
                        },
                        'marker': {
                            'radius': 0.68,
                        },
                        'text': {
                            'radius': 0.9,
                            'position': "",
                        },
                    },
                },
            },
        }

        self.set_container(chart_definition)

    def get_data(self):
        return self.get_container()
