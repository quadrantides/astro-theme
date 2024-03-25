# coding=utf-8
"""
Created on 2020, June 5th
@author: orion
"""
import os
import pandas as pd
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'astro.settings')
django.setup()

import numpy as np
import datetime

from plotly import graph_objects as go

from astro.planets.positions.from_swiss_ephemeris import get_planet_data, get_iflag, get_planet_index

from transcend.views.charts.theme.figure.processes import get_coordinates

from aspects.read import get as get_aspects
from aspects.read import get_internal_conjunctions

DATE_FORMAT = "%Y"

if __name__ == '__main__':

    width = 750
    height = width

    planet1 = 'sun'
    planet2 = "venus"

    planet_index = get_planet_index(planet1)

    angle = 0
    orb_value = 2
    start = datetime.datetime(1950, 1, 1, 0, 0)
    end = datetime.datetime(2000, 1, 1, 0, 0)
    conjunction_type = "superior"

    title = "Date des conjonctions supérieures de Vénus avec le Soleil entre {} et {}".format(
        1950,
        2000,
    )
    conjunctions = get_aspects(planet1, planet2, angle, start, end, orb_value=orb_value)

    nb_conjunctions = len(conjunctions)

    dates = [None] * nb_conjunctions
    longitudes = np.full(nb_conjunctions, 999.9)
    longitudes_in_zodiac = np.full(nb_conjunctions, 999.9)
    zodiac = [""] * nb_conjunctions
    types = [""] * nb_conjunctions

    for i, conjunction in enumerate(conjunctions):
        dt = conjunction.end-conjunction.start
        dates[i] = conjunction.start + dt/2.0
        longitude, latitude, distance, zodiaci, longitude_in_zodiac, is_retrograde = \
            get_planet_data(dates[i], planet_index, get_iflag())

        longitudes_in_zodiac[i] = longitude_in_zodiac
        zodiac[i] = zodiaci
        longitudes[i] = longitude
        rc, internal_conjunctions = get_internal_conjunctions(planet1, planet2, conjunction.id)
        if rc.success:
            types[i] = internal_conjunctions.type

    data = dict(
        zodiac=zodiac,
        longitude=longitudes,
        longitudes_in_zodiac=longitudes_in_zodiac,
        date=dates,
        type=types,
    )

    df = pd.DataFrame(data)
    # df.sort_values(["zodiac", "date"])

    df_filtered = df[df['type'] == conjunction_type]
    nb_conjunctions = len(df_filtered['longitude'])

    nb_loops = 0
    dangle = 0
    previous_longitude = 999.9
    loop_longitudes = []
    loop_number = 1
    loops = dict()
    for longitude in df_filtered['longitude']:
        if not previous_longitude == 999.9:
            wangle = longitude - previous_longitude
            if wangle < 0:
                dangle += longitude + (360 - previous_longitude)
            else:
                dangle += wangle

            if dangle >= 360:
                loops[loop_number] = loop_longitudes
                dangle = 0
                loop_longitudes = []
                loop_number += 1

        loop_longitudes.append(longitude)
        previous_longitude = longitude

    if len(loop_longitudes) > 0:
        loops[loop_number] = loop_longitudes

    nb_loops = list(loops.keys())[-1]
    categoryarray = 0.05 + 0.37 * np.array(list(range(nb_loops))) / (nb_loops - 1)

    text_based_colors = [""] * nb_loops

    r = np.full(nb_conjunctions, 999.9)
    text_colors = [""] * nb_conjunctions
    i = 0
    for key in loops.keys():
        for j in range(len(loops[key])):
            r[i] = categoryarray[key - 1]
            i += 1

    df_filtered.insert(5, "r", r, True)

    text = ['{}'.format(date.strftime(DATE_FORMAT)) for date in df_filtered["date"]]

    text_colors =""
    coordinates = [None] * nb_conjunctions
    for i in range(nb_conjunctions):
        coordinates[i] = get_coordinates(df_filtered['longitude'].to_list()[i], df_filtered['r'].to_list()[i])

    # print(df)
    t = go.Scatterpolar(
        visible=False,
        r=df_filtered['r'],
        theta=df_filtered['longitude'],
        mode='lines',
        name=planet2,
        text=text,
    )
    data = [t]

    annotations = [dict(
        x=0.5 + coordinatesi["x"],
        y=0.5 + coordinatesi["y"],
        text=texti,
        xanchor='center',
        yanchor='middle',
        showarrow=False,
    ) for coordinatesi, texti in zip(coordinates, text)]

    layout = go.Layout(
        title=title,
        width=width,
        height=height,
        font=dict(
            family='sans-serif',
            size=10,
            color='#000',
        ),
        annotations=annotations,
        xaxis=dict(
            fixedrange=True,
            visible=False,
        ),

        polar=dict(
            domain=dict(
                x=[0, 1],
                y=[0, 1],
            ),
            bgcolor="rgb(255, 2555, 255)",
            angularaxis=dict(
                visible=False,
                linewidth=1,
                showline=True,
                linecolor='#444',
                dtick=30,
                thetaunit="degrees",
                gridcolor="#444",
                gridwidth=1,
                # showticklabels=False,
                ticks='outside',
            ),
            radialaxis=dict(
                visible=False,
                tickmode="array",
                tickvals=2 * categoryarray,
                showticklabels=False,
                side="counterclockwise",
                angle=0,
                showline=False,
                linewidth=1,
                tickwidth=0,
                gridcolor="#444",
                gridwidth=1
            ),
        ),
    )

    fig = go.Figure(data=data, layout=layout)
    # fig = go.Figure(layout=layout)
    fig.write_html("test2.html")
