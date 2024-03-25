# coding=utf-8
"""
Created on 2020, Apr 3rd
@author: orion
"""
from openastromod import zonetab

from webservices.geonames.offline.connection import Connection


class Request(object):
    """
    Request

    """
    def __init__(self):

        self.connection = Connection()

    def get_connection(self):
        return self.connection

    def get_nearest_city(self, lat=None, lon=None):

        connection = self.get_connection()
        cursor = connection.get_cursor()

        res = {'country': None, 'admin1': None, 'geonameid': None, 'continent': None, 'timezonestr': None}

        if lat and lon:
            # get closest value to lat lon

            diff = {}
            sql = 'SELECT id,latitude,longitude ' \
                  'FROM geonames ' \
                  'WHERE latitude >= {} AND latitude <= {} AND longitude >= {} AND longitude <= {}'.format(
                    lat - 0.5,
                    lat + 0.5,
                    lon - 0.5,
                    lon + 0.5
                  )

            cursor.execute(sql)

            for row in cursor:
                diff[zonetab.distance(lat, lon, row['latitude'], row['longitude'])] = row['id']
            keys = list(diff.keys())
            keys.sort()

            res = {}
            if len(keys) > 0:
                sql = 'SELECT * FROM geonames WHERE id={} LIMIT 1'.format(diff[keys[0]])
                cursor.execute(sql)
                geoname = cursor.fetchone()
                res['countrycode'] = geoname['country']
                res['admin1'] = geoname['admin1']
                res['geonameid'] = geoname['geonameid']
                res['timezone'] = geoname['timezone']
                res['city'] = geoname['name']
                res['latitude'] = geoname['latitude']
                res['longitude'] = geoname['longitude']

                sql = "SELECT * FROM countryinfo WHERE isoalpha2='{}' LIMIT 1".format(
                    geoname['country'],
                )
                cursor.execute(sql)
                countryinfo = cursor.fetchone()
                res['continent'] = countryinfo['continent']
                # print('gnearest: found town %s at %s,%s,%s' % (geoname['name'], geoname['latitude'],
                #                                                 geoname['longitude'], geoname['timezone']))
        self.connection.close()
        return res

    def city_search(self, city):

        connection = self.get_connection()
        cursor = connection.get_cursor()

        # look for country in search string
        isoalpha2 = None
        if city.find(","):
            split = city.split(",")
            for x in range(len(split)):
                sql = "SELECT * FROM countryinfo WHERE \
    			(isoalpha2 LIKE ? OR name LIKE ?) LIMIT 1"
                y = split[x].strip()
                cursor.execute(sql, (y, y))
                result = cursor.fetchone()
                if result != None:
                    isoalpha2 = result["isoalpha2"]
                    city = city.replace(split[x] + ",", "").replace("," + split[x], "").strip()
                    # print "%s,%s"%(city,isoalpha2)
                    break

        # normal search
        normal = city
        fuzzy = "%" + city + "%"
        if isoalpha2:
            extra = " AND country='%s'" % (isoalpha2)
        else:
            extra = ""

        sql = "SELECT * FROM geonames WHERE \
    	(name LIKE ? OR asciiname LIKE ?)%s \
    	LIMIT 1" % (extra)
        cursor.execute(sql, (normal, normal))
        result = cursor.fetchone()

        if result == None:
            sql = "SELECT * FROM geonames WHERE \
    		(name LIKE ? OR asciiname LIKE ?)%s \
    		LIMIT 1" % (extra)
            cursor.execute(sql, (fuzzy, fuzzy))
            result = cursor.fetchone()

        if result == None:
            sql = "SELECT * FROM geonames WHERE \
    		(alternatenames LIKE ?)%s \
    		LIMIT 1" % (extra)
            cursor.execute(sql, (fuzzy,))
            result = cursor.fetchone()

        # if result != None:
        #     # set continent
        #     sql = "SELECT continent FROM countryinfo WHERE isoalpha2=? LIMIT 1"
        #     cursor.execute(sql, (result["country"],))
        #     self.contbox.set_active(self.searchcontinent[cursor.execute.fetchone()[0]])
        #     # set country
        #     self.countrybox.set_active(self.searchcountry[result["country"]])
        #     # set admin1
        #     self.provbox.set_active(self.searchprov[result["admin1"]])
        #     # set city
        #     self.citybox.set_active(self.searchcity[result["geonameid"]])

        return result


if __name__ == '__main__':

    req = Request()
    result = req.city_search("paris")
    print("ok")
