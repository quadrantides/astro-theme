# coding=utf-8
"""
Created on 2020, March 10th
@author: orion
"""
from transcend.processes import merge

from transcend.models.openastro.processes import Process as ModelProcess

from transcend.views.charts.graphics.constants import DIMENSIONS

from transcend.views.charts.theme.sidereal.graphics import Graphic as SiderealGraphicTheme
from transcend.views.charts.theme.tropical.graphics import Graphic as TropicalGraphicTheme
from transcend.views.charts.theme.compounded.graphics import Graphic as CompoundedGraphicTheme

from transcend.views.charts.transit.tropical.graphics import Graphic as TropicalGraphicTransit


def get_config():
    return dict(
        # staticPlot=True,
        modeBarButtonsToRemove=[
            "zoom2d",
            "pan2d",
            "select2d",
            "lasso2d",
            "zoomIn2d",
            "zoomOut2d",
            "autoScale2d",
            "resetScale2d",
            "hoverClosestPie",
            "toggleHover",
            "resetViews",
            "toggleSpikelines",
            "hoverClosestCartesian",
            "hoverCompareCartesian",

        ],
        # scrollZoom=False,
        # editable=False,
    )


class Process(object):

    def __init__(
            self,
            selection,
    ):
            self.model = ModelProcess(selection)
            self.processes = dict()
            self.graphics = dict()
            self.init()

            self.process()

    def init(self):
        self.graphics['sidereal'] = None
        self.graphics['tropical'] = None
        self.graphics['compounded'] = None

    def process(self):
        if self.model.tropical:
            self.create_tropical_graphic()
        if self.model.sidereal:
            self.create_sidereal_graphic()
        if self.model.tropical and self.model.sidereal:
            self.create_compounded_graphic()

    def get_tropical_selection(self):

        res = self.model.get_tropical_selection()

        # countries_data = get_countries_data(res['countrycode'])
        # res.update(countries_data)

        return res

    def get_sidereal_selection(self):

        res = self.model.get_sidereal_selection()

        # countries_data = get_countries_data(res['countrycode'])
        # res.update(countries_data)

        return res

    def create_compounded_graphic(self):
        title = "Tropical + Sidereal"
        name = 'compounded'
        self.graphics[name] = CompoundedGraphicTheme(
            self.model,
            title,
        )

    def get_chart_name(self, name):
        return 'transit' if self.model.has_transit_data(name) else "theme"

    def create_tropical_graphic(self):
        title = "Tropical"
        name = 'tropical'
        if self.get_chart_name(name) == "transit":
            self.graphics[name] = TropicalGraphicTransit(
                self.model,
                title,
            )
        elif self.get_chart_name(name) == "theme":
            self.graphics[name] = TropicalGraphicTheme(
                self.model,
                title,
            )

    def create_sidereal_graphic(self):

        name = 'sidereal'
        title = "Sidereal"

        self.graphics[name] = \
            SiderealGraphicTheme(
                self.model,
                title,
            )

    def get_context(self, json=True):
        tropical = self.graphics['tropical'].get_graphic(json=json) if self.graphics['tropical'] else dict()
        sidereal = self.graphics['sidereal'].get_graphic(json=json) if self.graphics['sidereal'] else dict()
        compounded = self.graphics['compounded'].get_graphic(json=json) if self.graphics['compounded'] else dict()

        return {
            'graphics': dict(
                tropical=tropical,
                sidereal=sidereal,
                compounded=compounded,
                config=get_config(),
            ),
            'cycles': self.get_cycles_data(),
        }

    def get_graphics_data(self):
        tropical = self.graphics['tropical'].get_graphic_data() if self.graphics['tropical'] else dict()
        sidereal = self.graphics['sidereal'].get_graphic_data() if self.graphics['sidereal'] else dict()
        compounded = self.graphics['compounded'].get_graphic_data() if self.graphics['compounded'] else dict()

        return {
            'graphics': dict(
                tropical=tropical,
                sidereal=sidereal,
                compounded=compounded,
                config=get_config(),
            ),
        }

    def get_cycles_data(self):
        return self.model.get_cycles()

    def get_data(self):
        res = dict()

        res['tropical_selection'] = self.get_tropical_selection()
        res['sidereal_selection'] = self.get_sidereal_selection()
        res['tropical_settings'] = self.model.get_tropical_settings()
        res['sidereal_settings'] = self.model.get_sidereal_settings()
        res['cycles'] = self.model.get_cycles()

        res = merge(
            dict(
                chart=dict(
                    color=DIMENSIONS['color'],
                ),
                planets=self.model.get_planets_names(),
            ),
            res,
        )

        return res
