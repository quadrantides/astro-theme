# coding=utf-8
"""
Created on 2020, June 1st
@author: orion
"""
import os
import datetime as dt
import numpy as np

from bokeh.models import HBar
from bokeh.layouts import gridplot
from bokeh.models.widgets import Div
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.io import curdoc, show, output_file, save
from bokeh.layouts import column
from bokeh.models import DatetimeTickFormatter
from bokeh.models import TickFormatter
from bokeh.models import Legend, Circle
from bokeh.models import HoverTool
from bokeh.models import FuncTickFormatter
from bokeh.palettes import Category10
from bokeh.core.properties import Dict, Int, String

from astro.utils import str_date_for_filename

from astro.constants import PLANETS_POSITION_OUTPUTS_HTML, QUADRANTIDES_BODIES
from astro.constants import ZODIAC_NAMES

DATE_FORMAT = "%Y%m%d%H%M"

HOVERTOOL_DATE_FORMAT = "%d/%B%Y"


def get_retrograde_indexes(is_retrograde):
    indexes = []
    for i, item in enumerate(is_retrograde):
        if item:
            indexes.append(i)
    return indexes


def get_hover_retrograde_period(begin_date, end_date):

    return "{} - {}".format(
            begin_date.strftime(format="%d %B %Y"),
            end_date.strftime(format="%d %B %Y"),

    )


def get_retrograde_periods(
        dates,
        is_retrograde,
):
    rindexes = get_retrograde_indexes(is_retrograde)
    nb_records = len(rindexes)
    retrograde_periods = np.array(["                                                     "] * nb_records)
    i = 0
    istep = 1
    begin_rindex = rindexes[i]
    jbegin = i
    previous_rindex = begin_rindex
    jprevious = jbegin
    i += istep
    eod = i >= nb_records
    periods = []
    while not eod:
        current_rindex = rindexes[i]
        j = i
        retrogradation_in_progress = (current_rindex - previous_rindex) == 1
        while not eod and retrogradation_in_progress:
            previous_rindex = current_rindex
            jprevious = j
            i += istep
            eod = i >= nb_records
            if not eod:
                current_rindex = rindexes[i]
                j = i
                retrogradation_in_progress = (current_rindex - previous_rindex) == 1
                print('ok')

        # rupture

        begin_date = dates[begin_rindex]
        end_date = dates[previous_rindex]

        for j in range(jbegin, jprevious + 1):
            retrograde_periods[j] = get_hover_retrograde_period(begin_date, end_date)


        # periods.append(
        #     (begin_date, end_date,),
        # )

        previous_rindex = current_rindex
        begin_rindex = current_rindex
        jprevious = j
        jbegin = j

        i += 1
        eod = i >= nb_records

    return retrograde_periods


def get_report(begin_date, end_date, planet):
    report = "<table>"
    # report += \
    #     "<tr><th colspan='2'>{}</th><th colspan='2'>{}</th><th colspan='2'>{}</th></tr>".format(
    #         "PLANÈTE",
    #         "DÉBUT",
    #         "FIN",
    #     )
    report += \
        "<tr><th colspan='2'>{}</th><td colspan='2'>du {}</td><td colspan='2'>au {}</td></tr>".format(
            planet,
            begin_date.strftime(format="%d/%m/%Y"),
            end_date.strftime(format="%d/%m/%Y"),

        )
    report += "</table>"
    return report


def get_reports(dates, is_retrograde, planet, timedelta=dt.timedelta(hours=24)):
    rindexes = get_retrograde_indexes(is_retrograde)
    # i = 0
    # begin_date = dates[rindexes[i]]
    # for ri in rindexes[1::]:
    #     le_frequency = ((dates[ri] - begin_date) - timedelta) <= 1e-5
    #     while
    #
    #
    # rdates = [dates[i] for i in rindexes]
    nb_records = len(rindexes)
    i = 0
    eod = i >= nb_records

    begin_rindex = rindexes[i]
    previous_rindex = begin_rindex
    i += 1
    eod = i >= nb_records
    reports = []
    while not eod:
        current_rindex = rindexes[i]
        retrogradation_in_progress = (current_rindex - previous_rindex) == 1
        while not eod and retrogradation_in_progress:
            previous_rindex = current_rindex
            i += 1
            eod = i >= nb_records
            if not eod:
                current_rindex = rindexes[i]
                retrogradation_in_progress = (current_rindex - previous_rindex) == 1
                print('ok')

        # rupture
        begin_date = dates[begin_rindex]
        end_date = dates[previous_rindex]

        reports.append(
            get_report(begin_date, end_date, planet),
        )

        previous_rindex = current_rindex
        begin_rindex = current_rindex

        i += 1
        eod = i >= nb_records


        # report = "<table>"
        # report += \
        #     "<tr><th colspan='2'>{}</th><th colspan='2'>{}</th></tr>".format(
        #         "DATES",
        #         planet,
        #     )
        # report += \
        #     "<tr><th colspan='2'>{}</th><th colspan='2'>{}</th></tr>".format(
        #         "DATES",
        #         planet,
        #     )
        #
        # for i, date in enumerate(dates):
        #     str_date = date.strftime(format="%d/%m/%Y %H:%M")
        #     report += \
        #         "<tr><td style='text-align: center;'>{}   </td><td style='text-align: center;'>{}   </td></tr>".format(
        #             str_date,
        #             is_retrograde[i],
        #         )
        # report += "</table>"
        # reports.append(report)
    return reports


def create(dates, is_retrograde, planet):

    p1 = is_retrograde

    str_start = str_date_for_filename(dates[0])
    str_end = str_date_for_filename(dates[-1])

    title = "Rétrogadation(s) entre le {} et le {}".format(
        dates[0].strftime(format="%d/%m/%Y"),
        dates[-1].strftime(format="%d/%m/%Y"),
    )

    filename = "{}.{}.{}.ts.{}.html".format(
        planet,
        str_start,
        str_end,
        dt.datetime.now().strftime(DATE_FORMAT),
    )

    fullfilename = os.path.join(
        PLANETS_POSITION_OUTPUTS_HTML,
        filename,
    )

    output_file(fullfilename)

    div_title_text = "<table>"
    div_title_text += \
        "<tr><th colspan='2'>{}</th></tr>".format(
            title,
        )
    div_title_text += "</table>"
    div_title = Div(text=div_title_text, width=800)

    div_planet_retrogradation_texts = get_reports(dates, is_retrograde, planet)

    divs = []
    for text in div_planet_retrogradation_texts:

        divs.append(
            Div(text=text, width=400),
        )

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
        legend_label=planet,
        source=source1,
    )

    p0.legend.location = "top_left"

    ##############
    # Show
    ##############
    # show(column([p0, p]))
    # show(column([p0]))
    divs.insert(0, div_title)
    save(column(divs))


def create_colored_timeserie(dates, bodies):

    # p1 = is_retrograde

    str_start = str_date_for_filename(dates[0])
    str_end = str_date_for_filename(dates[-1])

    title = "Retrograde Calendar {}".format(
        dates[0].year,
    )

    filename = "{}.{}.{}.ts.{}.html".format(
        "all_planets",
        str_start,
        str_end,
        dt.datetime.now().strftime(DATE_FORMAT),
    )

    fullfilename = os.path.join(
        PLANETS_POSITION_OUTPUTS_HTML,
        filename,
    )

    output_file(fullfilename)

    zodiac_offsets = dict()
    for i, zodiac in enumerate(ZODIAC_NAMES):
        zodiac_offsets[zodiac] = 30 * i

    x_range = [dates[0], dates[-1]]

    p0 = \
        figure(
            x_axis_type="datetime",
            x_axis_label='Date',
            y_axis_label='Zodiac',
            x_range=x_range,
            y_range=[0, 360],
            # title=title,
            width=1100,
            height=550,
            tools="crosshair,reset,box_zoom, pan",
        )
    p0.add_layout(Legend(), 'right')

    # retrograde_color = '#ff8080'
    # direct_color = '#00e64d'
    retrograde_color = '#6b6b47'
    direct_color = '#c2c2a3'
    renderers = []

    # QUADRANTIDES_BODIES.remove("moon")

    for i, body in enumerate(QUADRANTIDES_BODIES):

        retrograde_color = bodies[body]['color']
        direct_color = retrograde_color

        color = [retrograde_color if item else direct_color for item in bodies[body]['is_retrograde']]
        label = ['retrograde' if item else "direct" for item in bodies[body]['is_retrograde']]
        marker = ['dot' if item else "square" for item in bodies[body]['is_retrograde']]
        name = [body] * len(dates)
        zodiac = bodies[body]['zodiac']
        longitude_in_zodiac = bodies[body]['longitude_in_zodiac']
        y = [l + zodiac_offsets[z] % 360 for l, z in zip(longitude_in_zodiac, zodiac)]
        source = ColumnDataSource(data=dict(x=dates, y=y, color=color, label=label, marker=marker, name=name))

        if body == 'Asc' or body == "Mc":
            p0.line(
                x='x',
                y='y',
                color=direct_color,
                # fill_alpha=0.25,
                # alpha=0.25,
                legend_label='{}'.format(body.capitalize()),
                source=source,
            )
        else:
            size = 5 if body == "sun" else 1
            p0.circle(
                x='x',
                y='y',
                color=direct_color,
                # fill_alpha=0.25,
                # alpha=0.25,
                size=size,
                legend_label='{}'.format(body.capitalize()),
                source=source,
            )

        # retrograde

        indexes = [i for i, is_retrograde in enumerate(bodies[body]['is_retrograde']) if is_retrograde]

        if len(indexes) > 0:

            retrograde_periods = \
                get_retrograde_periods(
                    dates,
                    bodies[body]['is_retrograde'],
                )

            wdates = np.array(dates)[indexes]
            wy = np.array(y)[indexes]

            wname = [body] * len(indexes)
            wcolor = [retrograde_color] * len(indexes)
            # wlabel = ['{}'.format(body.capitalize())] * len(indexes)
            retrograde_longitude_in_zodiac = np.array(longitude_in_zodiac)[indexes]
            retrograde_zodiac = np.array(zodiac)[indexes]
            zodiac = []
            for z, l in zip(retrograde_zodiac, retrograde_longitude_in_zodiac):
                zodiac.append(
                    "{} {:6.2f}".format(
                        z,
                        l,
                    ),
                ),
            source = ColumnDataSource(
                data=dict(
                    x=wdates,
                    y=wy,
                    color=wcolor,
                    # label=wlabel,
                    name=wname,
                    retrograde_periods=retrograde_periods,
                    zodiac=zodiac,
                ),
            )

            circles = p0.circle(
                x='x',
                y='y',
                color="color",
                # legend_group="label",
                source=source,
            )
            renderers.append(circles)

    if len(renderers) > 0:
        hover = \
            HoverTool(
                renderers=renderers,
                tooltips=[
                    ("Planet", "@name"),
                    ("Date", "@x{%d %B %Y}"),
                    ("Zodiac", "@zodiac"),
                    ("R", "@retrograde_periods"),
                 ]
            )

        hover.formatters = {"@x": "datetime"}

        p0.add_tools(hover)

    p0.xaxis.formatter = DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )

    ybar = 30 * np.array(range(13)) - 15
    left = [x_range[0]] * 13
    right = [x_range[1]] * 13
    fill_color = [
        "#c2c2d6",
        "#fff",
        "#c2c2d6",
        "#fff",
        "#c2c2d6",
        "#fff",
        "#c2c2d6",
        "#fff",
        "#c2c2d6",
        "#fff",
        "#c2c2d6",
        "#fff",
        "#c2c2d6",
    ]

    source_bar = ColumnDataSource(dict(y=ybar, left=left, right=right, fill_color=fill_color,))

    glyph = HBar(y="y", right="right", left="left", height=30, fill_color="fill_color", fill_alpha=0.25, line_width=0)
    p0.add_glyph(source_bar, glyph)

    label_dict = {}
    ticker = []
    for i in range(len(ZODIAC_NAMES)):
        ticker.append(i * 30 + 15)
        label_dict[ticker[-1]] = ZODIAC_NAMES[i]

    p0.yaxis.ticker = ticker
    p0.yaxis.major_label_overrides = label_dict

    # p1 = gridplot([[p0]], toolbar_location=None)

    ##############
    # Show
    ##############

    # script, div = components(p0)
    # print(script)
    # print(div)

    ##############
    # Show
    ##############

    # show(column([p0]))

    # filename = "{}.{}.{}.ts.{}.html".format(
    #     "all_planets",
    #     str_start,
    #     str_end,
    #     dt.datetime.now().strftime(DATE_FORMAT),
    # )
    #
    # fullfilename = os.path.join(
    #     PLANETS_POSITION_OUTPUTS_HTML,
    #     filename,
    # )

    # output_file(fullfilename)
    # save(column([p0]))
    show(column([p0]))
