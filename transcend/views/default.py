# coding=utf-8
"""
Created on 2019, Dec 17th
@author: orion
"""
import plotly
import json
from pyramid.view import view_config

from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )

from pyramid.view import (
    view_config,
    view_defaults
    )

from transcend.security.security import (
    USERS,
    check_password
)

# from pyramid.httpexceptions import (
#     HTTPForbidden,
#     HTTPFound,
#     HTTPNotFound,
#     )

import datetime

from transcend.constants import DEBUG
from transcend.constants import DATE_FORMAT
from transcend.views.charts.theme.processes import Process
from transcend.views.location import get as get_location
from transcend.views.location import get_country_code

from transcend.models.openastro.models import SiderealDefault, TropicalDefault, OpenAstroInput

# from transcend.settings import get as get_settings

session = dict()
user = 'moi'
session[user] = dict(reader=None)


def get_filename(requestDataDict):
    return requestDataDict['filename']


def get_name(requestDataDict):
    return requestDataDict['title']


def get_date(requestDataDict):
    return requestDataDict['date']



@view_config(route_name='myview', renderer='../gabarit/Worthy-master/home.jinja2', require_csrf=False)
def myview(request):
    print('myview / ok')
    # Require CSRF Token
    # check_csrf_token(request)
    return dict()


@view_config(route_name='location', renderer='json')
def new_location(request):
    res = dict()
    data = request.POST
    has_data = len(list(data.values())) > 0
    if has_data:
        validated = validate(
            dict(data)
        )
        res = get_location(validated)

    return res


@view_config(route_name='load/theme', renderer='json', require_csrf=False)
def load_theme(request):
    res = dict()
    data = request.POST
    has_data = len(list(data.values())) > 0
    if has_data:
        validated = validate(
            dict(data)
        )

        sidereal = OpenAstroInput()
        sidereal.set_chartview("traditional")
        sidereal.set_sidereal_mode(validated['sidereal-mode'])
        sidereal.set_zodiactype("sidereal")
        sidereal.set_date(validated['date'])
        sidereal.set_timezonestr(validated['timezone'])
        sidereal.set_postype("geo")
        sidereal.set_houses_system(validated['sidereal-houses-system'])
        sidereal.set_location(validated['location'])
        sidereal.set_geolon(validated['longitude'])
        sidereal.set_geolat(validated['latitude'])
        sidereal.set_countrycode(
            get_country_code(validated['country']),
        )

        tropical = OpenAstroInput()
        tropical.set_zodiactype("tropical")
        tropical.set_chartview("traditional")
        tropical.set_date(validated['date'])
        tropical.set_timezonestr(validated['timezone'])
        tropical.set_postype("geo")
        tropical.set_houses_system(validated['tropical-houses-system'])
        tropical.set_location(validated['location'])
        tropical.set_geolon(validated['longitude'])
        tropical.set_geolat(validated['latitude'])
        tropical.set_countrycode(
            get_country_code(validated['country']),
        )

        selection = {
            'tropical': tropical,
            'sidereal': sidereal,
        }

    print("=========================== USER SELECTION report ======================================")
    zodiactype = "tropical"
    print()
    print(zodiactype.upper())
    current = selection[zodiactype].get_data()
    for key in current.keys():
        print(
            "{}:13 = {}".format(
                key,
                current[key],
            )
        )
    print()
    zodiactype = "sidereal"
    print(zodiactype.upper())
    current = selection[zodiactype].get_data()
    for key in current.keys():
        print(
            "{:13} = {}".format(
                key,
                current[key],
            )
        )
    print("=========================== USER SELECTION report ======================================")
    return get_openastro_data(selection)


# @view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
# def my_view(request):
#     return {'project': 'Mon projet : wrfio'}


# @view_config(route_name='home', renderer='../templates/home.jinja2')
# def home(request):
#     return dict()


# # @view_config(route_name='home', renderer='../static/node_modules/leaflet-draw/examples/good_index.jinja2')
# @view_config(route_name='home', renderer='../templates/leaflet-draw/good_index.jinja2')
# @view_config(route_name='home', renderer='../templates/index.jinja2')
@view_config(route_name='home', renderer='../gabarit/Worthy-master/home.jinja2')
def home(request):
    # token = new_csrf_token(request)
    if DEBUG:
        begin = datetime.datetime.now()
        print("BEGIN request treatment on server / date = {}".format(begin))

    data = request.POST
    has_data = len(list(data.values())) > 0
    if has_data:
        validated = validate(
            dict(data)
        )

        sidereal = OpenAstroInput()
        sidereal.set_chartview("traditional")
        sidereal.set_sidereal_mode(validated['sidereal-mode'])
        sidereal.set_zodiactype("sidereal")
        sidereal.set_date(validated['date'])
        sidereal.set_timezonestr(validated['timezone'])
        sidereal.set_postype("geo")
        sidereal.set_houses_system(validated['sidereal-houses-system'])
        sidereal.set_location(validated['location'])
        sidereal.set_geolon(validated['longitude'])
        sidereal.set_geolat(validated['latitude'])
        sidereal.set_countrycode(
            get_country_code(validated['country']),
        )

        tropical = OpenAstroInput()
        tropical.set_zodiactype("tropical")
        tropical.set_chartview("traditional")
        tropical.set_date(validated['date'])
        tropical.set_timezonestr(validated['timezone'])
        tropical.set_postype("geo")
        tropical.set_houses_system(validated['tropical-houses-system'])
        tropical.set_location(validated['location'])
        tropical.set_geolon(validated['longitude'])
        tropical.set_geolat(validated['latitude'])
        tropical.set_countrycode(
            get_country_code(validated['country']),
        )

        selection = {
            'tropical': tropical,
            'sidereal': sidereal,
        }

        context = get_openastro_data(selection)

    else:

        default_selection = {
            'tropical': TropicalDefault(),
            'sidereal': SiderealDefault(),
        }

        context = get_openastro_data(default_selection)

    context['title'] = 'Transcend Astrologies'

    if DEBUG:
        end = datetime.datetime.now()
        print("END request treatment on server / date = {}".format(end))

        duration = end - begin
        total_seconds = duration.total_seconds()
        if total_seconds > 1:
            total_seconds = int(total_seconds)

        print(
            "TREATMENTS DURATION SERVER SIDE = {} seconds".format(
                total_seconds,
            )
        )
    print("=========================== report ======================================")
    for k in context['data']['tropical_selection'].keys():
        print("{} : {}".format(k, context['data']['tropical_selection'][k]))
    # print("")
    # print("planets : location0 : {}".format(context['data']['planets']['locations'][0]))
    print("=========================== report ======================================")

    return context


# @view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
# def hello_world(request):
#     return Response('Hello World!')


def reformat_entered_date(date):
    day_suffixes = ['st', 'nd', 'rd', 'th']
    nsuffixes = len(day_suffixes)
    found = False
    eod = False
    i = 0
    while not found and not eod:
        day_suffix = day_suffixes[i]
        if date.find(day_suffix) != -1:
            found = True
        else:
            i += 1
        if i >= nsuffixes:
            eod = True
    if found:
        new_date = date.replace(day_suffix, "")
    else:
        raise Exception("Date format error")
    return new_date


def validate(data):

    if 'str_date' in data.keys():
        str_date = "{} {}".format(data["str_date"], data["str_time"])
        data['date'] = datetime.datetime.strptime(str_date, DATE_FORMAT)

    if 'longitude' in data.keys():
        data['longitude'] = float(data['longitude'])

    if 'latitude' in data.keys():
        data['latitude'] = float(data['latitude'])

    return data


def get_openastro_data(selection):

    process = Process(selection)
    return process.get_context()


def get_theme_context(data):

    context = dict()

    key = "entered_date"
    if key in data.keys():
        context['date'] = data[key]

    key = 'latitude'
    if key in data.keys():
        context[key] = "{:7.3f}".format(
            data[key],
        )

    key = 'longitude'
    if key in data.keys():
        context[key] = "{:7.3f}".format(
            data[key],
        )

    return context


# def get_pie_data(data, key):
    # houses = data[key].tolist()
    # end = houses[1::]
    # end.append(houses[0])
    # begin = houses
    # values = []
    # legend_values = []
    # for i, b in enumerate(begin):
    #     if end[i] > b:
    #         endi = end[i]
    #     else:
    #         endi = end[i] + 360
    #
    #     value = endi - b
    #     legend_value = b + (value / 2)
    #     values.append(value)
    #     legend_values.append(legend_value)
    #
    # pass
    # return {
    #     "rotation": 90 - houses[1],
    #     'values': values,
    #     'legend_values': legend_values,
    # }


# def add_context(data):
#
#     # add pie coordinates
#     key1 = 'houses'
#     key2 = 'zodiacs'
#
#     key = 'sidereal'
#     if key in data.keys():
#
#         pie_data = get_pie_data(data[key], key1)
#         data[key]['pie'] = {key1: pie_data}
#         pie_data = get_pie_data(data[key][key2], 'locations')
#         data[key]['pie'][key2] = pie_data
#
#     key = 'tropical'
#     if key in data.keys():
#         pie_data = get_pie_data(data[key], 'houses')
#         data[key]['pie'] = {key1: pie_data}
#         pie_data = get_pie_data(data[key][key2], 'locations')
#         data[key]['pie'][key2] = pie_data
#     return data

#
# @view_config(route_name='theme', renderer='../templates/theme.jinja2')
# def theme(request):
#
#     data = request.POST
#
#     validated = validate(data)
#
#     openastro_data = get_openastro_data(validated)
#
#     context = add_context(openastro_data)
#     context = openastro_data
#
#     return context


# @view_config(route_name='load/date', renderer='json')
# def get_data_by_date(request):
#     before = datetime.datetime.now()
#     requestDataDict = request.json
#     fullfilename = '{}/{}'.format(WRF_PATH, get_filename(requestDataDict))
#     if session[user]['reader'] is None:
#         session[user]['reader'] = EcmwfNetcdfReader(fullfilename, init=True)
#     time = session[user]['reader'].get_time()
#     var_name = get_name(requestDataDict)
#     str_date = get_date(requestDataDict)
#     if str_date == "":
#         time_index = 0
#     else:
#         str_time = [t.strftime("%Y-%m-%dT%H:%M:%S") for t in time['values']]
#         time_index = str_time.index(str_date)
#     # before = datetime.datetime.now()
#     # data = reader.get_geofeatures_by_date(var_name, time_index)
#     # print(datetime.datetime.now() - before)
#     data = session[user]['reader'].get_geodata_by_date_optimized(var_name, time_index)
#     print("Temps d'exécution de la fonction get_data_by_date : {}".format(datetime.datetime.now() - before))
#     return data
#
#
# @view_config(route_name='load', renderer='json')
# def load_json(request):
#     requestDataDict = request.json
#     fullfilename = '{}/{}'.format(WRF_PATH, get_filename(requestDataDict))
#     var_name = get_name(requestDataDict)
#     if not reader:
#         reader = EcmwfNetcdfReader(fullfilename, init=True)
#     data = reader.get_geofeatures(var_name, fullfilename)
#     return data


@view_config(route_name='login', renderer='../gabarit/Worthy-master/login.jinja2')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'  # never use login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        hashed_pw = USERS.get(login)
        if hashed_pw and check_password(password, hashed_pw):
            headers = remember(request, login)
            return HTTPFound(location=came_from,
                             headers=headers)
        message = 'Failed login'

    return dict(
        name='Login',
        message=message,
        url=request.application_url + '/login',
        came_from=came_from,
        login=login,
        password=password,
    )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    url = request.route_url('home')
    return HTTPFound(location=url,
                     headers=headers)
