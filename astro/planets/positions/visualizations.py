# coding=utf-8
"""
Created on 2020, June 12th
@author: orion
"""
import os
import numpy as np

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.io import curdoc, show, output_file
from bokeh.layouts import column
from bokeh.models import DatetimeTickFormatter
from bokeh.palettes import Category10

from astro.utils import str_date_for_filename

DATE_FORMAT = "%Y-%m-%d %H:%M"

ORBS = [2, 4, 6, 8, 10]
nb_orbs = len(ORBS)

if nb_orbs in Category10.keys():

    PALETTE = Category10[nb_orbs]

    COLORS = dict()
    for i, orb in enumerate(ORBS):

        colori = PALETTE[i]
        COLORS.update(
            {orb: colori}
        )

    else:
        nb_colors = 10
        PALETTE = Category10[nb_colors]

        COLORS = dict()
        for i, orb in enumerate(ORBS):
            colori = PALETTE[i] if i < nb_colors else nb_colors - 1
            COLORS.update(
                {orb: colori}
            )

imax = 4 * (nb_orbs + 1)

SIZES = dict()
for i, orb in enumerate(ORBS):
    SIZES.update(
        {orb: imax - 4 * i}
    )


def compare(dates, planet1, planet2, swe_longitudes, astropy_positions):


    astropy_position1 = astropy_positions[0]
    astropy_position2 = astropy_positions[1]

    swe_longitude1 = swe_longitudes[0]
    swe_longitude2 = swe_longitudes[1]

    title = "Comparaison des positions fournies par astropy et swiss ephemeris"

    filename = "{}.{}.html".format(
        planet1,
        planet2,
    )

    output_file(filename)

    p = \
        figure(
            x_axis_type="datetime",
            x_axis_label='Date',
            y_axis_label='Ascension droite / Position',
            title=title,
            width=900,
            height=450,
        )

    p.xaxis.formatter = \
        DatetimeTickFormatter(
            days=["%d/%m/%Y"],
            months=["%m/%Y"],
            hours=["%d/%m/%Y %H"],
            minutes=["%d/%m/%Y %H:%M"]
        )

    y1 = swe_longitude1 - astropy_position1
    source1 = ColumnDataSource(data=dict(x=dates, y=y1))

    p.square(
        x='x',
        y='y',
        color="red",
        legend_label=planet1,
        source=source1,
    )

    y2 = swe_longitude2 - astropy_position2
    source2 = ColumnDataSource(data=dict(x=dates, y=y2))

    p.square(
        x='x',
        y='y',
        color="green",
        legend_label=planet2,
        source=source2,
    )

    ##############
    # Show
    ##############
    show(p)

