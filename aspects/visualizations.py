# coding=utf-8
"""
Created on 2020, June 1st
@author: orion
"""
import os
from datetime import datetime
import numpy as np

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.io import curdoc, show, output_file, save
from bokeh.layouts import column
from bokeh.models import DatetimeTickFormatter
from bokeh.palettes import Category10

from astro.utils import str_date_for_filename

from .constants import ASPECTS_OUTPUTS_HTML

DATE_FORMAT = "%Y%m%d%H%M"

ORBS = [2, 3, 4, 6, 8, 10]
nb_orbs = len(ORBS)

nb_colors = 10
PALETTE = Category10[nb_colors]

COLORS = dict()
for i, orb in enumerate(ORBS):
    colori = PALETTE[i] if i < nb_colors else nb_colors - 1
    COLORS.update(
        {orb: colori}
    )

COLORS = {2: "#000000", 3: "#cc0000", 4: "#ff6600", 6: "#ffbf00", 8: "#ff80ff", 10: '#0080ff'}


def aspects(dates, right_ascensions, planet1, planet2, aspects=None):

    p1 = np.array(right_ascensions[0])
    p2 = np.array(right_ascensions[1])

    str_start = str_date_for_filename(dates[0])
    str_end = str_date_for_filename(dates[-1])

    title = "Cycle : {} - {}".format(
        planet1,
        planet2,
    )

    if aspects:
        angles = [item.get_container().angle for item in aspects]
        angles = np.unique(angles)
        angles = sorted(angles)
        title = "{} - Angles = {}".format(
            title,
            ", ".join([str(angle) for angle in angles]),
        )

    filename = "{}.{}.{}.{}.ts.{}.html".format(
        planet1,
        planet2,
        str_start,
        str_end,
        datetime.now().strftime(DATE_FORMAT),
    )

    fullfilename = os.path.join(
        ASPECTS_OUTPUTS_HTML,
        filename,
    )

    output_file(fullfilename)

    p0 = \
        figure(
            x_axis_type="datetime",
            x_axis_label='Date',
            y_axis_label='Ascension droite',
            title=title,
            width=900,
            height=450,
        )

    source1 = ColumnDataSource(data=dict(x=dates, y=p1))

    p0.circle(
        x='x',
        y='y',
        color="#ffbf00",
        legend_label=planet1,
        source=source1,
    )

    source2 = ColumnDataSource(data=dict(x=dates, y=p2))
    p0.square(
        x='x',
        y='y',
        color="#ff0080",
        legend_label=planet2,
        source=source2,
    )

    p0.legend.location = "top_left"

    p = \
        figure(
            x_axis_type="datetime",
            x_axis_label='Date',
            y_axis_label='Distance angulaire',
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

    y = p1 - p2
    # y = np.array([yi % 360 for yi in y])
    source = ColumnDataSource(data=dict(x=dates, y=y))

    p.square(
        x='x',
        y='y',
        color="#B2DF8A",
        legend_label="observation",
        source=source,
    )

    if aspects:

        data = dict()
        for orb in ORBS:
            data.update(
                {orb: dict(start=[], end=[], angle=[])}
            )

        for item in aspects:
            aspect = item.get_container()
            orb = aspect.orb
            data[orb]["start"].append(
                aspect.start,
            )
            data[orb]["end"].append(
                aspect.end,
            )
            data[orb]["angle"].append(
                aspect.angle,
            )

        sorbs = sorted(data.keys())
        sorbs.reverse()
        for key in sorbs:
            if len(data[key]["start"]) > 0:
                legend_label = "aspect ({})".format(
                    key,
                )
                aspect_dates = []
                aspect_y = []
                aspect_color = []

                for start, end in zip(data[key]["start"], data[key]["end"]):
                    if key == 6:
                        print("ok")
                    indexes = np.where((dates >= start) & (dates <= end))[0]
                    aspect_dates.extend(
                        dates[indexes],
                    )

                    aspect_y.extend(
                        y[indexes],
                    )

                    aspect_color.extend(
                        [COLORS[key]] * len(indexes),
                    )

                sindexes = np.argsort(aspect_dates)
                source = ColumnDataSource(
                    data=dict(
                        x=np.array(aspect_dates)[sindexes],
                        y=np.array(aspect_y)[sindexes],
                        color=aspect_color,
                    ),
                )

                p.circle(
                    x='x',
                    y='y',
                    color='color',
                    legend_label=legend_label,
                    source=source,
                    # fill_color='color',
                    size=8,
                )

        p.legend.location = "top_left"

    ##############
    # Show
    ##############
    # show(column([p0, p]))
    save(column([p0, p]))
