# coding=utf-8
"""
Created on 2020, Apr 5rd
@author: orion
"""
import geoname


if __name__ == '__main__':
    city = "vienne"
    country_code = 'fr'
    result = geoname.search(city, country_code)
    print(result)
