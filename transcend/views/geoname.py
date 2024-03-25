# coding=utf-8
"""
Created on 2020, April 6th
@author: orion
"""
from webservices.geonames.offline.request import Request
# from transcend.file.countries.reader import Reader as FileCountriesReader
#
#
# def get_country_code(name):
#     reader = FileCountriesReader()
#     return reader.get_code(name)
#
#
# def get_countries_data(code):
#
#     reader = FileCountriesReader()
#     countries = reader.get_names()
#
#     country_index = reader.get_country_index(code)
#
#     return dict(countries=countries, country_index=country_index)


def get(lat, lon):
    req = Request()
    res = req.get_nearest_city(
        lat=lat,
        lon=lon,
    )
    # add country
    # res.update(
    #     get_countries_data(res['countrycode'])
    # )

    return res
