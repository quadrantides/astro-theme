# coding=utf-8
"""
Created on 2020, April 16th
@author: orion
"""
import pandas as pd
import datetime
import plotly.express as px
from plotly.subplots import make_subplots

from astro.constants import BODIES_COLORS


def get_body_color(body):
    return BODIES_COLORS[body]


# def get_data():
#     data = dict(
#         year=[
#             "2020", "2020", "2020", "2020", "2020", "2020",
#             "2020", "2020",
#             "2020", "2020",
#             "2020", "2020",
#             "2020", "2020",
#             "2020", "2020",
#             "2020", "2020",
#             "2020", "2020",
#         ],
#         retrograde=[
#             "Retrograde 1", "Retrograde 1", "Retrograde 2", "Retrograde 2", "Retrograde 3", "Retrograde 3",
#             "Retrograde 1", "Retrograde 1",
#             "Retrograde 1", "Retrograde 1",
#             "Retrograde 1", "Retrograde 1",
#             "Retrograde 1", "Retrograde 1",
#             "Retrograde 1", "Retrograde 1",
#             "Retrograde 1", "Retrograde 1",
#             "Retrograde 1", "Retrograde 1",
#         ],
#
#         planet=[
#             "Mercury", "Mercury", "Mercury", "Mercury", "Mercury", "Mercury",
#             "Venus", "Venus",
#             "Mars", "Mars",
#             "Jupiter", "Jupiter",
#             "Saturn", "Saturn",
#             'Uranus', 'Uranus',
#             "Neptune", "Neptune",
#             "Pluto", "Pluto",
#         ],
#         date=[
#             "17/02/2020", "12/03/2020", "17/06/2020", "15/07/2020", "16/10/2020", "06/11/2020",
#             "11/05/2020", "26/06/2020",
#             "10/09/2020", "15/11/2020",
#             "07/05/2020", "15/09/2020",
#             "20/09/2020", "20/02/2020",
#             "30/08/2020", "31/12/2020",
#             "20/06/2020", "11/12/2020",
#             "22/04/2020", "14/09/2020",
#         ],
#         zodiac=[
#             "pisces 12°62", 'aquarius 29°18', "cancer 14°47", "cancer 5°23", 'scorpio 11°14', "libra 27°36",
#             "gemini", "gemini",
#             "aries", 'aries',
#             "capricorn", "capricorn",
#             "aquarius", "capricorn",
#             "taurus", "taurus",
#             "pisces", "pisces",
#             "capricorn", "capricorn",
#         ],
#
#     )
#
#     return pd.DataFrame(data)

def get_date_retrogrades():
    return dict(
        mercury=[
            dict(
                start=datetime.datetime(2008, 1, 8, 0, 0),
                end=datetime.datetime(2008, 2, 1, 0, 0),
            ),
            dict(
                start=datetime.datetime(2008, 1, 8, 0, 0),
                end=datetime.datetime(2008, 2, 1, 0, 0),
            ),
        ]
    )
def get_data():
    data = dict(
        year=[
            "2020",
            "2020",
            "2020",
            "2020",
            # "2020",
            # "2020",
            # "2020",
            # "2020",
            # "2020",
            # "2020",
        ],
        retrograde=[
            "1",
            "2",
            "3",
            "1",
            # "",
            # "",
            # "",
            # "",
            # "",
            # "",
        ],

        contents=[
            "{:10} {:5} {:12}<BR>{:10} {:5} {:12}".format(
                "17/02/2020",
                "12°62",
                "pisces",
                "12/03/2020",
                "29°18",
                "aquarius",

            ),
            "{:10} {:5} {:12}<BR>{:10} {:5} {:12}".format(
                "17/02/2020",
                "12°62",
                "pisces",
                "12/03/2020",
                "29°18",
                "aquarius",

            ),
            "{:10} {:5} {:12}<BR>{:10} {:5} {:12}".format(
                "17/02/2020",
                "12°62",
                "pisces",
                "12/03/2020",
                "29°18",
                "aquarius",

            ),
            "{:10} {:5} {:12}<BR>{:10} {:5} {:12}".format(
                "17/02/2020",
                "12°62",
                "pisces",
                "12/03/2020",
                "29°18",
                "aquarius",

            ),
            # "",
            # "",
            # "",
            # "",
            # "",
            # "",
        ],

        planet=[
            "Mercury",
            "Mercury",
            "Mercury",
            "Venus",
            # "Mars",
            # "Jupiter",
            # "Saturn",
            # 'Uranus',
            # "Neptune",
            # "Pluto",
        ],
        # date=[
        #     "17/02/2020", "12/03/2020", "17/06/2020", "15/07/2020", "16/10/2020", "06/11/2020",
        #     "11/05/2020", "26/06/2020",
        #     "10/09/2020", "15/11/2020",
        #     "07/05/2020", "15/09/2020",
        #     "20/09/2020", "20/02/2020",
        #     "30/08/2020", "31/12/2020",
        #     "20/06/2020", "11/12/2020",
        #     "22/04/2020", "14/09/2020",
        # ],
        # zodiac=[
        #     "17/02/2020 pisces 12°62\n12/03/2020 aquarius 29°18", "17/02/2020 pisces 12°62\n12/03/2020 aquarius 29°18", "cancer 14°47", "cancer 5°23", 'scorpio 11°14', "libra 27°36",
        #     "gemini", "gemini",
        #     "aries", 'aries',
        #     "capricorn", "capricorn",
        #     "aquarius", "capricorn",
        #     "taurus", "taurus",
        #     "pisces", "pisces",
        #     "capricorn", "capricorn",
        # ],
        #
        # begin=[
        #     "17/02/2020 pisces 12°62", "17/02/2020 pisces 12°62",
        #     "cancer 14°47", "cancer 5°23", 'scorpio 11°14', "libra 27°36",
        #     "gemini", "gemini",
        #     "aries", 'aries',
        #     "capricorn", "capricorn",
        #     "aquarius", "capricorn",
        #     "taurus", "taurus",
        #     "pisces", "pisces",
        #     "capricorn", "capricorn",
        # ],
        #
        # end=[
        #     "12/03/2020 aquarius 29°18", "12/03/2020 aquarius 29°18",
        #     "cancer 14°47", "cancer 5°23", 'scorpio 11°14', "libra 27°36",
        #     "gemini", "gemini",
        #     "aries", 'aries',
        #     "capricorn", "capricorn",
        #     "aquarius", "capricorn",
        #     "taurus", "taurus",
        #     "pisces", "pisces",
        #     "capricorn", "capricorn",
        # ],

    )

    return pd.DataFrame(data)


def get_data2():
    data = dict(
        year=[
            "2020", "2020", "2020", "2020", "2020", "2020",
            "2020", "2020",
            "2020", "2020",
            "2020", "2020",
            "2020", "2020",
            "2020", "2020",

        ],
        retrograde=[
            "Retrograde 1", "Retrograde 1", "Retrograde 2", "Retrograde 2", "Retrograde 3", "Retrograde 3",
            "Retrograde 1", "Retrograde 1",
            "Retrograde 1", "Retrograde 1",
            "Retrograde 1", "Retrograde 1",
            "Retrograde 1", "Retrograde 1",
            "Retrograde 1", "Retrograde 1",

        ],

        planet=[
            "Mercury", "Mercury", "Mercury", "Mercury", "Mercury", "Mercury",
            "Venus", "Venus",
            "Mars", "Mars",
            "Jupiter", "Jupiter",
            "Saturn", "Saturn",
            'Uranus', 'Uranus',

        ],
        date=[
            "17/02/2020", "12/03/2020", "17/06/2020", "15/07/2020", "16/10/2020", "06/11/2020",
            "11/05/2020", "26/06/2020",
            "10/09/2020", "15/11/2020",
            "07/05/2020", "15/09/2020",
            "20/09/2020", "20/02/2020",
            "30/08/2020", "31/12/2020",

        ],
        zodiac=[
            "pisces 12°62", 'aquarius 29°18', "cancer 14°47", "cancer 5°23", 'scorpio 11°14', "libra 27°36",
            "gemini", "gemini",
            "aries", 'aries',
            "capricorn", "capricorn",
            "aquarius", "capricorn",
            "taurus", "taurus",

        ],

    )

    return pd.DataFrame(data)


df = get_data()

fig = px.treemap(
    df,
    # path=["year", 'planet', 'retrograde', "date", "zodiac"],
    path=["year", 'planet', 'retrograde', 'contents'],

    # values='end',
    # color='color',
    color_discrete_map={
        '(?)': 'white',
        'Mercury': get_body_color("mercury"),
        'Mars': get_body_color("mars"),
        'Venus': get_body_color("venus"),
        'Jupiter': get_body_color("jupiter"),
        'Saturn': get_body_color("saturn"),
        'Uranus': get_body_color("uranus"),
        'Neptune': get_body_color("neptune"),
        'Pluto': get_body_color("pluto"),

    },
)

fig.layout.hovermode = False

# colors=[
#     'black',
#     "#fff",
#     get_body_color("mars"),
#     get_body_color("venus"),
#     get_body_color("jupiter"),
#     get_body_color("saturn"),
#     get_body_color("uranus"),
#     get_body_color("neptune"),
#     get_body_color("pluto"),
# ]

colors=[
    'yellow',
    get_body_color("mercury"),
    get_body_color("mercury"),
]

data = fig.data[0]

# fig.update_traces(marker_colors=colors, selector=dict(type='treemap'))
# fig.update_traces(=0.25, selector=dict(type='treemap'))

df2 = get_data()

fig2 = px.treemap(
    df2,
    path=["year", 'planet', 'retrograde', 'contents'],
    # values='end',
    color='planet',
    color_discrete_map={
        '(?)': 'white',
        'Mercury': "yellow",
        'Mars': get_body_color("mars"),
        'Venus': get_body_color("venus"),
        'Jupiter': get_body_color("jupiter"),
        'Saturn': get_body_color("saturn"),
        'Uranus': get_body_color("uranus"),
        'Neptune': get_body_color("neptune"),
        'Pluto': get_body_color("pluto"),

    },
)

trace2 = fig2.data[0]

fig.update_traces(trace2, selector=dict(type='treemap'))

fig.write_html(
    "{}.html".format(
        "modern",
    ),
)
