#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    This file is part of openastro.org.

    OpenAstro.org is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenAstro.org is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with OpenAstro.org.  If not, see <http://www.gnu.org/licenses/>.
"""

# basics
import numpy
import copy
import math, sys, os.path, datetime, socket, gettext, codecs, webbrowser, pytz

# copyfile
from shutil import copyfile

# pysqlite
import sqlite3

sqlite3.dbapi2.register_adapter(str, lambda s: s.decode('utf-8'))

# template processing
from string import Template

# minidom parser
from xml.dom.minidom import parseString

from openastromod import zonetab, geoname, importfile, dignities, swiss as ephemeris

from transcend.constants import ASTROLIB_DB, GEONAMES_DB, DATE_FORMAT, PLANETS_OF_INTEREST
from transcend.views.constants import HOUSES_ICONS

from astro.utils import convert_degrees_minutes, convert_degrees_minutes_seconds
# debug
LOCAL = False
DEBUG = False
VERSION = '1.1.57'


# directories
# if LOCAL:
#     DATADIR=os.path.dirname(__file__)
# elif os.path.exists(os.path.join(sys.prefix,'share','openastro.org')):
#     DATADIR=os.path.join(sys.prefix,'share','openastro.org')
# elif os.path.exists(os.path.join("/", 'usr','local','share','openastro.org')):
#     DATADIR=os.path.join("/", 'usr','local','share','openastro.org')
# elif os.path.exists(os.path.join("/", 'usr','share','openastro.org')):
#     DATADIR=os.path.join("/", 'usr','share','openastro.org')
# else:
#     print("Exiting... can't find data directory")
#     sys.exit()


# Translations
# LANGUAGES_LABEL={
#             "ar":"الْعَرَبيّة",
#             "pt_BR":"Português brasileiro",
#             "bg":"български език",
#             "ca":"català",
#             "cs":"čeština",
#             "da":"dansk",
#             "nl":"Nederlands",
#             "eo":"Esperanto",
#             "en":"English",
#             "fi":"suomi",
#             "fr":"Français",
#             "de":"Deutsch",
#             "el":"ελληνικά",
#             "hu":"magyar nyelv",
#             "it":"Italiano",
#             "ja":"日本",
#             "nds":"Plattdüütsch",
#             "nb":"Bokmål",
#             "pl":"język polski",
#             "rom":"rromani ćhib",
#             "ru":"Русский",
#             "es":"Español",
#             "sv":"svenska",
#             "uk":"українська мова",
#             "zh_TW":"正體字"
#         }

# TDomain = os.path.join(DATADIR,'locale')
# LANGUAGES=list(LANGUAGES_LABEL.keys())
# TRANSLATION={}
# for i in range(len(LANGUAGES)):
#     try:
#         TRANSLATION[LANGUAGES[i]] = gettext.translation("openastro",TDomain,languages=[LANGUAGES[i]])
#     except IOError as err:
#         print("IOError! Invalid languages specified (%s) in %s" %(LANGUAGES[i],TDomain))
#         TRANSLATION[LANGUAGES[i]] = gettext.translation("openastro",TDomain,languages=['en'])
#
# try:
#     TRANSLATION["default"] = gettext.translation("openastro",TDomain)
# except IOError as err:
#     print("OpenAstro.org has not yet been translated in your language! Could not load translation...")
#     TRANSLATION["default"] = gettext.translation("openastro",TDomain,languages=['en'])

# debug print function
def dprint(str):
    if "--debug" in sys.argv or DEBUG:
        print('%s' % str)


# config class
class openAstroCfg:

    def __init__(self):
        self.version = VERSION
        self.homedir = os.path.expanduser("~")

        # check for astrodir
        self.astrodir = os.path.join(self.homedir, '.openastro.org')
        if os.path.isdir(self.astrodir) == False:
            os.mkdir(self.astrodir)

        # check for tmpdir
        self.tmpdir = os.path.join(self.astrodir, 'tmp')
        if os.path.isdir(self.tmpdir) == False:
            os.mkdir(self.tmpdir)

        # check for swiss local dir
        self.swissLocalDir = os.path.join(self.astrodir, 'swiss_ephemeris')
        if os.path.isdir(self.swissLocalDir) == False:
            os.mkdir(self.swissLocalDir)

        # geonames database
        self.geonamesdb = GEONAMES_DB

        # icons
        # icons = os.path.join(DATADIR,'icons')
        # self.iconWindow = os.path.join(icons, 'openastro.svg')
        # self.iconAspects = os.path.join(icons, 'aspects')

        # basic files
        # self.tempfilename = os.path.join(self.tmpdir,"openAstroChart.svg")
        # self.tempfilenameprint = os.path.join(self.tmpdir,"openAstroChartPrint.svg")
        # self.tempfilenametable = os.path.join(self.tmpdir,"openAstroChartTable.svg")
        # self.tempfilenametableprint = os.path.join(self.tmpdir,"openAstroChartTablePrint.svg")
        # self.xml_ui = os.path.join(DATADIR, 'openastro-ui.xml')
        # self.xml_svg = os.path.join(DATADIR, 'openastro-svg.xml')
        # self.xml_svg_table = os.path.join(DATADIR, 'openastro-svg-table.xml')

        # sqlite databases
        self.astrodb = ASTROLIB_DB
        # self.peopledb = os.path.join(self.astrodir, 'peopledb.sql')
        # self.famousdb = os.path.join(DATADIR, 'famous.sql' )
        return

    def checkSwissEphemeris(self, num):
        # 00 = -01-600
        # 06 = 600 - 1200
        # 12 = 1200 - 1800
        # 18 = 1800 - 2400
        # 24 = 2400 - 3000
        seas = 'ftp://ftp.astro.com/pub/swisseph/ephe/seas_12.se1'
        semo = 'ftp://ftp.astro.com/pub/swisseph/ephe/semo_12.se1'
        sepl = 'ftp://ftp.astro.com/pub/swisseph/ephe/sepl_12.se1'


cfg = openAstroCfg()


# Sqlite database
class openAstroSqlite:
    def __init__(self):
        self.dbcheck = False
        self.dbpurge = "IGNORE"

        # --dbcheck puts dbcheck to true
        if "--dbcheck" in sys.argv:
            self.dbcheck = True

        # --purge purges database
        if "--purge" in sys.argv:
            self.dbcheck = True
            self.dbpurge = "REPLACE"

        self.open()
        # get table names from sqlite_master for astrodb
        sql = 'SELECT name FROM sqlite_master'
        self.cursor.execute(sql)
        list = self.cursor.fetchall()
        self.tables = {}
        for i in range(len(list)):
            self.tables[list[i][0]] = 1

        # get table names from sqlite_master for peopledb
        # sql='SELECT name FROM sqlite_master'
        # self.pcursor.execute(sql)
        # list=self.pcursor.fetchall()
        # self.ptables={}
        # for i in range(len(list)):
        #         self.ptables[list[i][0]]=1

        # check for event_natal table in peopledb
        # self.ptable_event_natal = {
        #     "id":"INTEGER PRIMARY KEY",
        #     "name":"VARCHAR(50)",
        #     "year":"VARCHAR(4)",
        #     "month":"VARCHAR(2)",
        #     "day":"VARCHAR(2)",
        #     "hour":"VARCHAR(50)",
        #     "geolon":"VARCHAR(50)",
        #     "geolat":"VARCHAR(50)",
        #     "altitude":"VARCHAR(50)",
        #     "location":"VARCHAR(150)",
        #     "timezone":"VARCHAR(50)",
        #     "notes":"VARCHAR(500)",
        #     "image":"VARCHAR(250)",
        #     "countrycode":"VARCHAR(2)",
        #     "geonameid":"INTEGER",
        #     "timezonestr":"VARCHAR(100)",
        #     "extra":"VARCHAR(500)"
        #     }
        # if 'event_natal' not in self.ptables:
        #     sql='CREATE TABLE IF NOT EXISTS event_natal (id INTEGER PRIMARY KEY,name VARCHAR(50)\
        #          ,year VARCHAR(4),month VARCHAR(2), day VARCHAR(2), hour VARCHAR(50), geolon VARCHAR(50)\
        #         ,geolat VARCHAR(50), altitude VARCHAR(50), location VARCHAR(150), timezone VARCHAR(50)\
        #         ,notes VARCHAR(500), image VARCHAR(250), countrycode VARCHAR(2), geonameid INTEGER\
        #         ,timezonestr VARCHAR(100), extra VARCHAR(250))'
        #     self.pcursor.execute(sql)
        #     dprint('creating sqlite table event_natal in peopledb')

        # check for astrocfg table in astrodb
        if 'astrocfg' not in self.tables:
            # 0=cfg_name, 1=cfg_value
            sql = 'CREATE TABLE IF NOT EXISTS astrocfg (name VARCHAR(150) UNIQUE,value VARCHAR(150))'
            self.cursor.execute(sql)
            self.dbcheck = True
            dprint('creating sqlite table astrocfg in astrodb')

        # check for astrocfg version
        sql = 'INSERT OR IGNORE INTO astrocfg (name,value) VALUES(?,?)'
        self.cursor.execute(sql, ("version", cfg.version))
        # get astrocfg dict
        sql = 'SELECT value FROM astrocfg WHERE name="version"'
        self.cursor.execute(sql)
        self.astrocfg = {}
        self.astrocfg["version"] = self.cursor.fetchone()[0]

        # check for updated version
        if self.astrocfg['version'] != str(cfg.version):
            dprint('version mismatch(%s != %s), checking table structure' % (self.astrocfg['version'], cfg.version))
            # insert current version and set dbcheck to true
            self.dbcheck = True
            sql = 'INSERT OR REPLACE INTO astrocfg VALUES("version","' + str(cfg.version) + '")'
            self.cursor.execute(sql)

        # default astrocfg keys (if dbcheck)
        if self.dbcheck:
            dprint('dbcheck astrodb.astrocfg')
            default = {
                "version": str(cfg.version),
                "use_geonames.org": "0",
                "houses_system": "P",
                "language": "default",
                "postype": "geo",
                "chartview": "traditional",
                "zodiactype": "tropical",
                "siderealmode": "FAGAN_BRADLEY"
            }
            for k, v in default.items():
                sql = 'INSERT OR %s INTO astrocfg (name,value) VALUES(?,?)' % (self.dbpurge)
                self.cursor.execute(sql, (k, v))

        # get astrocfg dict
        sql = 'SELECT * FROM astrocfg'
        self.cursor.execute(sql)
        self.astrocfg = {}
        for row in self.cursor:
            self.astrocfg[row['name']] = row['value']

        # install language
        # self.setLanguage(self.astrocfg['language'])
        # self.lang_label=LANGUAGES_LABEL
        #
        #
        # #fix inconsitencies between in people's database
        # if self.dbcheck:
        #     sql='PRAGMA table_info(event_natal)'
        #     self.pcursor.execute(sql)
        #     list=self.pcursor.fetchall()
        #     vacuum = False
        #     cnames=[]
        #     for i in range(len(list)):
        #         cnames.append(list[i][1])
        #     for key,val in self.ptable_event_natal.items():
        #         if key not in cnames:
        #             sql = 'ALTER TABLE event_natal ADD %s %s'%(key,val)
        #             dprint("dbcheck peopledb.event_natal adding %s %s"%(key,val))
        #             self.pcursor.execute(sql)
        #             vacuum = True
        #     if vacuum:
        #         sql = "VACUUM"
        #         self.pcursor.execute(sql)
        #         dprint('dbcheck peopledb.event_natal: updating table definitions!')

        # check for history table in astrodb
        if 'history' not in self.tables:
            # 0=id,1=name,2=year,3=month,4=day,5=hour,6=geolon,7=geolat,8=alt,9=location,10=tz
            sql = 'CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY,name VARCHAR(50)\
                 ,year VARCHAR(50),month VARCHAR(50), day VARCHAR(50), hour VARCHAR(50), geolon VARCHAR(50)\
                ,geolat VARCHAR(50), altitude VARCHAR(50), location VARCHAR(150), timezone VARCHAR(50)\
                ,notes VARCHAR(500), image VARCHAR(250), countrycode VARCHAR(2), geonameid INTEGER, extra VARCHAR(250))'
            self.cursor.execute(sql)
            dprint('creating sqlite table history in astrodb')

        # fix inconsitencies between 0.6x and 0.7x in history table
        if self.dbcheck:
            sql = 'PRAGMA table_info(history)'
            self.cursor.execute(sql)
            list = self.cursor.fetchall()
            cnames = []
            for i in range(len(list)):
                cnames.append(list[i][1])
            vacuum = False
            if "notes" not in cnames:
                sql = 'ALTER TABLE history ADD notes VARCHAR(500)'
                self.cursor.execute(sql)
                vacuum = True
            if "image" not in cnames:
                sql = 'ALTER TABLE history ADD image VARCHAR(250)'
                self.cursor.execute(sql)
                vacuum = True
            if "countrycode" not in cnames:
                sql = 'ALTER TABLE history ADD countrycode VARCHAR(2)'
                self.cursor.execute(sql)
                vacuum = True
            if "geonameid" not in cnames:
                sql = 'ALTER TABLE history ADD geonameid INTEGER'
                self.cursor.execute(sql)
                vacuum = True
            if "extra" not in cnames:
                sql = 'ALTER TABLE history ADD extra VARCHAR(250)'
                self.cursor.execute(sql)
                vacuum = True
            if vacuum:
                sql = "VACUUM"
                self.cursor.execute(sql)
                dprint('dbcheck: updating history table definitions!')

        # check for settings_aspect table in astrodb
        if 'settings_aspect' not in self.tables:
            sql = 'CREATE TABLE IF NOT EXISTS settings_aspect (degree INTEGER UNIQUE, name VARCHAR(50)\
                 ,color VARCHAR(50),visible INTEGER, visible_grid INTEGER\
                 ,is_major INTEGER, is_minor INTEGER, orb VARCHAR(5))'
            self.cursor.execute(sql)
            self.dbcheck = True
            dprint('creating sqlite table settings_aspect in astrodb')

        # if update, check if everything is in order
        if self.dbcheck:
            sql = 'PRAGMA table_info(settings_aspect)'
            self.cursor.execute(sql)
            list = self.cursor.fetchall()
            cnames = []
            for i in range(len(list)):
                cnames.append(list[i][1])
            vacuum = False
            if "visible" not in cnames:
                sql = 'ALTER TABLE settings_aspect ADD visible INTEGER'
                self.cursor.execute(sql)
                vacuum = True
            if "visible_grid" not in cnames:
                sql = 'ALTER TABLE settings_aspect ADD visible_grid INTEGER'
                self.cursor.execute(sql)
                vacuum = True
            if "is_major" not in cnames:
                sql = 'ALTER TABLE settings_aspect ADD is_major INTEGER'
                self.cursor.execute(sql)
                vacuum = True
            if "is_minor" not in cnames:
                sql = 'ALTER TABLE settings_aspect ADD is_minor INTEGER'
                self.cursor.execute(sql)
                vacuum = True
            if "orb" not in cnames:
                sql = 'ALTER TABLE settings_aspect ADD orb VARCHAR(5)'
                self.cursor.execute(sql)
                vacuum = True
            if vacuum:
                sql = "VACUUM"
                self.cursor.execute(sql)

        # default values for settings_aspect (if dbcheck)
        if self.dbcheck:
            dprint('dbcheck astrodb.settings_aspect')
            degree = [0, 30, 45, 60, 72, 90, 120, 135, 144, 150, 180]
            name = ['conjunction', 'semi-sextile', 'semi-square', 'sextile', 'quintile', 'square', 'trine',
                    'sesquiquadrate', 'biquintile', 'quincunx', 'opposition']
            color = ['#5757e2', '#810757', '#b14e58', '#d59e28', '#1f99b3', '#dc0000', '#36d100', '#985a10', '#7a9810',
                     '#fff600', '#510060']
            visible = [1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1]
            visible_grid = [1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1]
            is_major = [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1]
            is_minor = [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0]
            orb = [10, 3, 3, 6, 2, 8, 8, 3, 2, 3, 10]
            # insert values
            for i in range(len(degree)):
                sql = 'INSERT OR %s INTO settings_aspect \
                (degree, name, color, visible, visible_grid, is_major, is_minor, orb)\
                VALUES(%s,"%s","%s",%s,%s,%s,%s,"%s")' % (self.dbpurge, degree[i], name[i], color[i], visible[i],
                                                          visible_grid[i], is_major[i], is_minor[i], orb[i])
                self.cursor.execute(sql)

        # check for colors table in astrodb
        if 'color_codes' not in self.tables:
            sql = 'CREATE TABLE IF NOT EXISTS color_codes (name VARCHAR(50) UNIQUE\
                 ,code VARCHAR(50))'
            self.cursor.execute(sql)
            self.dbcheck = True
            dprint('creating sqlite table color_codes in astrodb')

        # default values for colors (if dbcheck)
        self.defaultColors = {
            "paper_0": "#000000",
            "paper_1": "#ffffff",
            "zodiac_bg_0": "#482900",
            "zodiac_bg_1": "#6b3d00",
            "zodiac_bg_2": "#5995e7",
            "zodiac_bg_3": "#2b4972",
            "zodiac_bg_4": "#c54100",
            "zodiac_bg_5": "#2b286f",
            "zodiac_bg_6": "#69acf1",
            "zodiac_bg_7": "#ffd237",
            "zodiac_bg_8": "#ff7200",
            "zodiac_bg_9": "#863c00",
            "zodiac_bg_10": "#4f0377",
            "zodiac_bg_11": "#6cbfff",
            "zodiac_icon_0": "#482900",
            "zodiac_icon_1": "#6b3d00",
            "zodiac_icon_2": "#5995e7",
            "zodiac_icon_3": "#2b4972",
            "zodiac_icon_4": "#c54100",
            "zodiac_icon_5": "#2b286f",
            "zodiac_icon_6": "#69acf1",
            "zodiac_icon_7": "#ffd237",
            "zodiac_icon_8": "#ff7200",
            "zodiac_icon_9": "#863c00",
            "zodiac_icon_10": "#4f0377",
            "zodiac_icon_11": "#6cbfff",
            "zodiac_radix_ring_0": "#ff0000",
            "zodiac_radix_ring_1": "#ff0000",
            "zodiac_radix_ring_2": "#ff0000",
            "zodiac_transit_ring_0": "#ff0000",
            "zodiac_transit_ring_1": "#ff0000",
            "zodiac_transit_ring_2": "#0000ff",
            "zodiac_transit_ring_3": "#0000ff",
            "houses_radix_line": "#ff0000",
            "houses_transit_line": "#0000ff",
            "aspect_0": "#5757e2",
            "aspect_30": "#810757",
            "aspect_45": "#b14e58",
            "aspect_60": "#d59e28",
            "aspect_72": "#1f99b3",
            "aspect_90": "#dc0000",
            "aspect_120": "#36d100",
            "aspect_135": "#985a10",
            "aspect_144": "#7a9810",
            "aspect_150": "#fff600",
            "aspect_180": "#510060",
            "planet_0": "#984b00",
            "planet_1": "#150052",
            "planet_2": "#520800",
            "planet_3": "#400052",
            "planet_4": "#540000",
            "planet_5": "#47133d",
            "planet_6": "#124500",
            "planet_7": "#6f0766",
            "planet_8": "#06537f",
            "planet_9": "#713f04",
            "planet_10": "#4c1541",
            "planet_11": "#4c1541",
            "planet_12": "#331820",
            "planet_13": "#585858",
            "planet_14": "#000000",
            "planet_15": "#666f06",
            "planet_16": "#000000",
            "planet_17": "#000000",
            "planet_18": "#000000",
            "planet_19": "#000000",
            "planet_20": "#000000",
            "planet_21": "#000000",
            "planet_22": "#000000",
            "planet_23": "#ff7e00",
            "planet_24": "#FF0000",
            "planet_25": "#0000FF",
            "planet_26": "#000000",
            "planet_27": "#000000",
            "planet_28": "#000000",
            "planet_29": "#000000",
            "planet_30": "#000000",
            "planet_31": "#000000",
            "planet_32": "#000000",
            "planet_33": "#000000",
            "planet_34": "#000000",
            "lunar_phase_0": "#000000",
            "lunar_phase_1": "#FFFFFF",
            "lunar_phase_2": "#CCCCCC"
        }
        if self.dbcheck:
            dprint('dbcheck astrodb.color_codes')
            # insert values
            for k, v in self.defaultColors.items():
                sql = 'INSERT OR %s INTO color_codes \
                (name, code)\
                VALUES("%s","%s")' % (self.dbpurge, k, v)
                self.cursor.execute(sql)

        # check for label table in astrodb
        if 'label' not in self.tables:
            sql = 'CREATE TABLE IF NOT EXISTS label (name VARCHAR(150) UNIQUE\
                 ,value VARCHAR(200))'
            self.cursor.execute(sql)
            self.dbcheck = True
            dprint('creating sqlite table label in astrodb')

        # default values for label (if dbcheck)
        self.defaultLabel = {
            "cusp": "Cusp",
            "longitude": "Longitude",
            "latitude": "Latitude",
            "north": "North",
            "east": "East",
            "south": "South",
            "west": "West",
            "apparent_geocentric": "Apparent Geocentric",
            "true_geocentric": "True Geocentric",
            "topocentric": "Topocentric",
            "heliocentric": "Heliocentric",
            "fire": "Fire",
            "earth": "Earth (element)",
            "air": "Air",
            "water": "Water",
            "radix": "Radix",
            "transit": "Transit",
            "synastry": "Synastry",
            "composite": "Composite",
            "combine": "Combine",
            "solar": "Solar",
            "secondary_progressions": "Secondary Progressions"
        }
        if self.dbcheck:
            dprint('dbcheck astrodb.label')
            # insert values
            for k, v in self.defaultLabel.items():
                sql = 'INSERT OR %s INTO label \
                (name, value)\
                VALUES("%s","%s")' % (self.dbpurge, k, v)
                self.cursor.execute(sql)

        # check for settings_planet table in astrodb
        self.table_settings_planet = {
            "id": "INTEGER UNIQUE",
            "name": "VARCHAR(50)",
            "color": "VARCHAR(50)",
            "visible": "INTEGER",
            "element_points": "INTEGER",
            "zodiac_relation": "VARCHAR(50)",
            "label": "VARCHAR(50)",
            "label_short": "VARCHAR(20)",
            "visible_aspect_line": "INTEGER",
            "visible_aspect_grid": "INTEGER"
        }
        if 'settings_planet' not in self.tables:
            sql = 'CREATE TABLE IF NOT EXISTS settings_planet (id INTEGER UNIQUE, name VARCHAR(50)\
                ,color VARCHAR(50),visible INTEGER, element_points INTEGER, zodiac_relation VARCHAR(50)\
                ,label VARCHAR(50), label_short VARCHAR(20), visible_aspect_line INTEGER\
                ,visible_aspect_grid INTEGER)'
            self.cursor.execute(sql)
            self.dbcheck = True
            dprint('creating sqlite table settings_planet in astrodb')

        # default values for settings_planet (if dbcheck)
        if self.dbcheck:
            dprint('dbcheck astrodb.settings_planet')
            self.value_settings_planet = {}
            self.value_settings_planet['name'] = [
                'sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn',
                'uranus', 'neptune', 'pluto', 'mean node', 'true node', 'mean apogee', 'osc. apogee',
                'earth', 'chiron', 'pholus', 'ceres', 'pallas', 'juno', 'vesta',
                'intp. apogee', 'intp. perigee', 'Asc', 'Mc', 'Dsc', 'Ic', 'day pars',
                'night pars', 'south node', 'marriage pars', 'black sun', 'vulcanus', 'persephone',
                'true lilith']
            orb = [
                # sun
                '{0:10,180:10,90:10,120:10,60:6,30:3,150:3,45:3,135:3,72:1,144:1}',
                # moon
                '{0:10,180:10,90:10,120:10,60:6,30:3,150:3,45:3,135:3,72:1,144:1}',
                # mercury
                '{0:10,180:10,90:10,120:10,60:6,30:3,150:3,45:3,135:3,72:1,144:1}',
                # venus
                '{0:10,180:10,90:10,120:10,60:6,30:3,150:3,45:3,135:3,72:1,144:1}',
                # mars
                '{0:10,180:10,90:10,120:10,60:6,30:3,150:3,45:3,135:3,72:1,144:1}',
                # jupiter
                '{0:10,180:10,90:10,120:10,60:6,30:3,150:3,45:3,135:3,72:1,144:1}',
                # saturn
                '{0:10,180:10,90:10,120:10,60:6,30:3,150:3,45:3,135:3,72:1,144:1}',
                # uranus
                '{0:10,180:10,90:10,120:10,60:6,30:3,150:3,45:3,135:3,72:1,144:1}',
                # neptunus
                '{0:10,180:10,90:10,120:10,60:6,30:3,150:3,45:3,135:3,72:1,144:1}',
                # pluto
                '{0:10,180:10,90:10,120:10,60:6,30:3,150:3,45:3,135:3,72:1,144:1}'
            ]
            self.value_settings_planet['label'] = [
                'Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn',
                'Uranus', 'Neptune', 'Pluto', 'North Node', '?', 'Lilith', 'Osc. Lilith',
                'Earth', 'Chiron', 'Pholus', 'Ceres', 'Pallas', 'Juno', 'Vesta',
                'intp. apogee', 'intp. perigee', 'Asc', 'Mc', 'Dsc', 'Ic', 'Day Pars',
                'Night Pars', 'South Node', 'Marriage Pars', 'Black Sun', 'Vulcanus',
                'Persephone', 'True Lilith']
            self.value_settings_planet['label_short'] = [
                'sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn',
                'uranus', 'neptune', 'pluto', 'Node', '?', 'Lilith', '?',
                'earth', 'chiron', 'pholus', 'ceres', 'pallas', 'juno', 'vesta',
                'intp. apogee', 'intp. perigee', 'Asc', 'Mc', 'Dsc', 'Ic', 'DP',
                'NP', 'SNode', 'marriage', 'blacksun', 'vulcanus', 'persephone', 'truelilith']
            self.value_settings_planet['color'] = [
                '#984b00', '#150052', '#520800', '#400052', '#540000', '#47133d', '#124500',
                '#6f0766', '#06537f', '#713f04', '#4c1541', '#4c1541', '#33182', '#000000',
                '#000000', '#666f06', '#000000', '#000000', '#000000', '#000000', '#000000',
                '#000000', '#000000', 'orange', '#FF0000', '#0000FF', '#000000', '#000000',
                '#000000', '#000000', '#000000', '#000000', '#000000', '#000000', '#000000']
            self.value_settings_planet['visible'] = [
                1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 0, 1, 0,
                0, 1, 0, 0, 0, 0, 0,
                0, 0, 1, 1, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0]
            self.value_settings_planet['visible_aspect_line'] = [
                1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 0, 1, 0,
                0, 1, 0, 0, 0, 0, 0,
                0, 0, 1, 1, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0]
            self.value_settings_planet['visible_aspect_grid'] = [
                1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 0, 1, 0,
                0, 1, 0, 0, 0, 0, 0,
                0, 0, 1, 1, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0]
            self.value_settings_planet['element_points'] = [
                40, 40, 15, 15, 15, 10, 10,
                10, 10, 10, 20, 0, 0, 0,
                0, 5, 0, 0, 0, 0, 0,
                0, 0, 40, 20, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0]
            # zodiac relation gives 10 extra points in element calculation
            self.value_settings_planet['zodiac_relation'] = [
                '4', '3', '2,5', '1,6', '0', '8', '9',
                '10', '11', '7', '-1', '-1', '-1', '-1',
                '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                '-1', '-1', '-1', '-1', '-1', '-1', '-1']

            # if update, check if everything is in order with settings_planet
            sql = 'PRAGMA table_info(settings_planet)'
            self.cursor.execute(sql)
            list = self.cursor.fetchall()
            vacuum = False
            cnames = []
            for i in range(len(list)):
                cnames.append(list[i][1])
            for key, val in self.table_settings_planet.items():
                if key not in cnames:
                    sql = 'ALTER TABLE settings_planet ADD %s %s' % (key, val)
                    dprint("dbcheck astrodb.settings_planet adding %s %s" % (key, val))
                    self.cursor.execute(sql)
                    # update values for col
                    self.cursor.execute("SELECT id FROM settings_planet ORDER BY id DESC LIMIT 1")
                    c = self.cursor.fetchone()[0] + 1
                    for rowid in range(c):
                        sql = 'UPDATE settings_planet SET %s=? WHERE id=?' % (key)
                        self.cursor.execute(sql, (self.value_settings_planet[key][rowid], rowid))
                    vacuum = True
            if vacuum:
                sql = "VACUUM"
                self.cursor.execute(sql)

            # insert values for planets that don't exists
            for i in range(len(self.value_settings_planet['name'])):
                sql = 'INSERT OR %s INTO settings_planet VALUES(?,?,?,?,?,?,?,?,?,?)' % (self.dbpurge)
                values = (i,
                          self.value_settings_planet['name'][i],
                          self.value_settings_planet['color'][i],
                          self.value_settings_planet['visible'][i],
                          self.value_settings_planet['element_points'][i],
                          self.value_settings_planet['zodiac_relation'][i],
                          self.value_settings_planet['label'][i],
                          self.value_settings_planet['label_short'][i],
                          self.value_settings_planet['visible_aspect_line'][i],
                          self.value_settings_planet['visible_aspect_grid'][i]
                          )
                self.cursor.execute(sql, values)

        # commit initial changes
        # self.updateHistory()
        self.link.commit()
        # self.plink.commit()
        self.close()

    # def setLanguage(self, lang=None):
    #     if lang==None or lang=="default":
    #         TRANSLATION["default"].install()
    #         dprint("installing default language")
    #     else:
    #         TRANSLATION[lang].install()
    #         dprint("installing language (%s)"%(lang))
    #     return

    def addHistory(self):
        self.open()
        sql = 'INSERT INTO history \
            (id,name,year,month,day,hour,geolon,geolat,altitude,location,timezone,countrycode) VALUES \
            (null,?,?,?,?,?,?,?,?,?,?,?)'
        tuple = (openAstro.name, openAstro.year, openAstro.month, openAstro.day, openAstro.hour,
                 openAstro.geolon, openAstro.geolat, openAstro.altitude, openAstro.location,
                 openAstro.timezone, openAstro.countrycode)
        self.cursor.execute(sql, tuple)
        self.link.commit()
        self.updateHistory()
        self.close()

    def getAstrocfg(self, key):
        self.open()
        sql = 'SELECT value FROM astrocfg WHERE name="%s"' % key
        self.cursor.execute(sql)
        one = self.cursor.fetchone()
        self.close()
        if one == None:
            return None
        else:
            return one[0]

    def setAstrocfg(self, key, val):
        sql = 'INSERT OR REPLACE INTO astrocfg (name,value) VALUES (?,?)'
        self.query([sql], [(key, val)])
        self.astrocfg[key] = val
        return

    def getColors(self):
        self.open()
        sql = 'SELECT * FROM color_codes'
        self.cursor.execute(sql)
        list = self.cursor.fetchall()
        out = {}
        for i in range(len(list)):
            out[list[i][0]] = list[i][1]
        self.close()
        return out

    def getLabel(self):
        self.open()
        sql = 'SELECT * FROM label'
        self.cursor.execute(sql)
        list = self.cursor.fetchall()
        out = {}
        for i in range(len(list)):
            out[list[i][0]] = list[i][1]
        self.close()
        return out

    # def getDatabase(self):
    #     self.open()
    #
    #     sql = 'SELECT * FROM event_natal ORDER BY id ASC'
    #     self.pcursor.execute(sql)
    #     dict = []
    #     for row in self.pcursor:
    #         s={}
    #         for key,val in self.ptable_event_natal.items():
    #             if row[key] == None:
    #                 s[key]=""
    #             else:
    #                 s[key]=row[key]
    #         dict.append(s)
    #     self.close()
    #     return dict

    # def getDatabaseFamous(self,limit="2000",search=None):
    #     self.flink = sqlite3.connect(cfg.famousdb)
    #     self.flink.row_factory = sqlite3.Row
    #     self.fcursor = self.flink.cursor()
    #
    #     if search:
    #         sql='SELECT * FROM famous WHERE year>? AND \
    #         (lastname LIKE ? OR firstname LIKE ? OR name LIKE ?)\
    #          LIMIT %s'%(limit)
    #         self.fcursor.execute(sql,(1800,search,search,search))
    #     else:
    #         sql='SELECT * FROM famous WHERE year>? LIMIT %s'%(limit)
    #         self.fcursor.execute(sql,(1800,))
    #
    #     oldDB=self.fcursor.fetchall()
    #
    #     self.fcursor.close()
    #     self.flink.close()
    #
    #     #process database
    #     newDB = []
    #     for a in range(len(oldDB)):
    #         #minus years
    #         if oldDB[a][12] == '571/': #Muhammad
    #             year = 571
    #         elif oldDB[a][12] <= 0:
    #             year = 1
    #         else:
    #             year = oldDB[a][12]
    #
    #         month = oldDB[a][13]
    #         day = oldDB[a][14]
    #         hour = oldDB[a][15]
    #         h,m,s = openAstro.decHour(hour)
    #
    #         #aware datetime object
    #         dt_input = datetime.datetime(year,month,day,h,m,s)
    #         dt = pytz.timezone(oldDB[a][20]).localize(dt_input)
    #
    #         #naive utc datetime object
    #         dt_utc = dt.replace(tzinfo=None) - dt.utcoffset()
    #         #timezone
    #         timezone=openAstro.offsetToTz(dt.utcoffset())
    #         year = dt_utc.year
    #         month = dt_utc.month
    #         day = dt_utc.day
    #         hour = openAstro.decHourJoin(dt_utc.hour,dt_utc.minute,dt_utc.second)
    #
    #         newDB.append({
    #                     "id":oldDB[a][0], #id INTEGER
    #                     "name":str(a+1)+". "+oldDB[a][3]+" "+oldDB[a][4], #name
    #                     "year":year, #year
    #                     "month":month, #month
    #                     "day":day, #day
    #                     "hour":hour, #hour
    #                     "geolon":oldDB[a][18], #geolon
    #                     "geolat":oldDB[a][17], #geolat
    #                     "altitude":"25", #altitude
    #                     "location":oldDB[a][16], #location
    #                     "timezone":timezone, #timezone
    #                     "notes":"",#notes
    #                     "image":"",#image
    #                     "countrycode":oldDB[a][8], #countrycode
    #                     "geonameid":oldDB[a][19], #geonameid
    #                     "timezonestr":oldDB[a][20], #timezonestr
    #                     "extra":"" #extra
    #                     })
    #
    #     return newDB

    def getSettingsPlanet(self):
        self.open()
        sql = 'SELECT * FROM settings_planet ORDER BY id ASC'
        self.cursor.execute(sql)
        dict = []
        for row in self.cursor:
            s = {}
            for key, val in self.table_settings_planet.items():
                if key == "label" or key == "label_short" or key == "name":
                    s[key] = row[key].lower()
                else:
                    s[key] = row[key]
            dict.append(s)
        self.close()
        return dict

    def getSettingsAspect(self):
        self.open()
        sql = 'SELECT * FROM settings_aspect ORDER BY degree ASC'
        self.cursor.execute(sql)
        dict = []
        for row in self.cursor:
            # degree, name, color, visible, visible_grid, is_major, is_minor, orb
            dict.append({'degree': row['degree'], 'name': row['name'], 'color': row['color']
                            , 'visible': row['visible'], 'visible_grid': row['visible_grid']
                            , 'is_major': row['is_major'], 'is_minor': row['is_minor'], 'orb': row['orb']})
        self.close()
        return dict

    def getSettingsLocation(self):
        # look if location is known
        if 'home_location' not in self.astrocfg or 'home_timezonestr' not in self.astrocfg:
            self.open()
            sql = 'INSERT OR REPLACE INTO astrocfg (name,value) VALUES("home_location","")'
            self.cursor.execute(sql)
            sql = 'INSERT OR REPLACE INTO astrocfg (name,value) VALUES("home_geolat","")'
            self.cursor.execute(sql)
            sql = 'INSERT OR REPLACE INTO astrocfg (name,value) VALUES("home_geolon","")'
            self.cursor.execute(sql)
            sql = 'INSERT OR REPLACE INTO astrocfg (name,value) VALUES("home_countrycode","")'
            self.cursor.execute(sql)
            sql = 'INSERT OR REPLACE INTO astrocfg (name,value) VALUES("home_timezonestr","")'
            self.cursor.execute(sql)
            self.link.commit()
            self.close
            return '', '', '', '', ''
        else:
            return self.astrocfg['home_location'], self.astrocfg['home_geolat'], self.astrocfg['home_geolon'], \
                   self.astrocfg['home_countrycode'], self.astrocfg['home_timezonestr']

    def setSettingsLocation(self, lat, lon, loc, cc, tzstr):
        self.open()
        sql = 'UPDATE astrocfg SET value="%s" WHERE name="home_location"' % loc
        self.cursor.execute(sql)
        sql = 'UPDATE astrocfg SET value="%s" WHERE name="home_geolat"' % lat
        self.cursor.execute(sql)
        sql = 'UPDATE astrocfg SET value="%s" WHERE name="home_geolon"' % lon
        self.cursor.execute(sql)
        sql = 'UPDATE astrocfg SET value="%s" WHERE name="home_countrycode"' % cc
        self.cursor.execute(sql)
        sql = 'UPDATE astrocfg SET value="%s" WHERE name="home_timezonestr"' % tzstr
        self.cursor.execute(sql)
        self.link.commit()
        self.close()

    def updateHistory(self):
        sql = 'SELECT * FROM history'
        self.cursor.execute(sql)
        self.history = self.cursor.fetchall()
        # check if limit is exceeded
        limit = 10
        if len(self.history) > limit:
            sql = "DELETE FROM history WHERE id < '" + str(self.history[len(self.history) - limit][0]) + "'"
            self.cursor.execute(sql)
            self.link.commit()
            # update self.history
            sql = 'SELECT * FROM history'
            self.cursor.execute(sql)
            self.history = self.cursor.fetchall()
        return

    """

    Function to import zet8 databases

    """

    def importZet8(self, target_db, data):

        target_con = sqlite3.connect(target_db)
        target_con.row_factory = sqlite3.Row
        target_cur = target_con.cursor()

        # get target names
        target_names = {}
        sql = 'SELECT name FROM event_natal'
        target_cur.execute(sql)
        for row in target_cur:
            target_names[row['name']] = 1
        for k, v in target_names.items():
            for i in range(1, 10):
                if '%s (#%s)' % (k, i) in target_names:
                    target_names[k] += 1

        # read input write target
        for row in data:

            if row['name'] in target_names:
                name_suffix = ' (#%s)' % target_names[row['name']]
                target_names[row['name']] += 1
            else:
                name_suffix = ''

            gname = self.gnearest(float(row['latitude']), float(row['longitude']))

            sql = 'INSERT INTO event_natal (id,name,year,month,day,hour,geolon,geolat,altitude,\
                location,timezone,notes,image,countrycode,geonameid,timezonestr,extra) VALUES \
                (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
            tuple = (row['name'] + name_suffix, row['year'], row['month'], row['day'], row['hour'], row['longitude'],
                     row['latitude'], 25, row['location'], row['timezone'], "",
                     "", gname['geonameid'], gname['timezonestr'], "")
            target_cur.execute(sql, tuple)

        # Finished, close connection
        target_con.commit()
        target_cur.close()
        target_con.close()

        return

    """

    Function to merge two databases containing entries for persons
    databaseMerge(target_db,input_db)

    database format:
    'CREATE TABLE IF NOT EXISTS event_natal (id INTEGER PRIMARY KEY,name VARCHAR(50)\
                 ,year VARCHAR(4),month VARCHAR(2), day VARCHAR(2), hour VARCHAR(50), geolon VARCHAR(50)\
                ,geolat VARCHAR(50), altitude VARCHAR(50), location VARCHAR(150), timezone VARCHAR(50)\
                ,notes VARCHAR(500), image VARCHAR(250), countrycode VARCHAR(2), geonameid INTEGER\
                ,timezonestr VARCHAR(100), extra VARCHAR(250))'
    """

    def databaseMerge(self, target_db, input_db):
        dprint('db.databaseMerge: %s << %s' % (target_db, input_db))
        target_con = sqlite3.connect(target_db)
        target_con.row_factory = sqlite3.Row
        target_cur = target_con.cursor()
        input_con = sqlite3.connect(input_db)
        input_con.row_factory = sqlite3.Row
        input_cur = input_con.cursor()
        # get target names
        target_names = {}
        sql = 'SELECT name FROM event_natal'
        target_cur.execute(sql)
        for row in target_cur:
            target_names[row['name']] = 1
        for k, v in target_names.items():
            for i in range(1, 10):
                if '%s (#%s)' % (k, i) in target_names:
                    target_names[k] += 1

        # read input write target
        sql = 'SELECT * FROM event_natal'
        input_cur.execute(sql)
        for row in input_cur:
            if row['name'] in target_names:
                name_suffix = ' (#%s)' % target_names[row['name']]
                target_names[row['name']] += 1
            else:
                name_suffix = ''
            sql = 'INSERT INTO event_natal (id,name,year,month,day,hour,geolon,geolat,altitude,\
                location,timezone,notes,image,countrycode,geonameid,timezonestr,extra) VALUES \
                (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
            tuple = (row['name'] + name_suffix, row['year'], row['month'], row['day'], row['hour'], row['geolon'],
                     row['geolat'], row['altitude'], row['location'], row['timezone'], row['notes'],
                     row['image'], row['countrycode'], row['geonameid'], row['timezonestr'], row['extra'])
            target_cur.execute(sql, tuple)

        # Finished, close connection
        target_con.commit()
        target_cur.close()
        target_con.close()
        input_cur.close()
        input_con.close()
        return

    """

    Basic Query Functions for common databases

    """

    def query(self, sql, tuple=None):
        l = sqlite3.connect(cfg.astrodb)
        c = l.cursor()
        for i in range(len(sql)):
            if tuple == None:
                c.execute(sql[i])
            else:
                c.execute(sql[i], tuple[i])
        l.commit()
        c.close()
        l.close()

    def pquery(self, sql, tuple=None):
        l = sqlite3.connect(cfg.peopledb)
        c = l.cursor()
        for i in range(len(sql)):
            if tuple == None:
                c.execute(sql[i])
            else:
                c.execute(sql[i], tuple[i])
        l.commit()
        c.close()
        l.close()

    def gnearest(self, lat=None, lon=None):
        # check for none
        if lat == None or lon == None:
            return {'country': None, 'admin1': None, 'geonameid': None, 'continent': None, 'timezonestr': None}
        # get closest value to lat lon
        dprint('gnearest: using %s,%s' % (lat, lon))
        diff = {}
        sql = 'SELECT id,latitude,longitude FROM geonames WHERE latitude >= %s AND latitude <= %s AND longitude >= %s AND longitude <= %s' % (
        lat - 0.5, lat + 0.5, lon - 0.5, lon + 0.5)
        self.gquery(sql)
        for row in self.gcursor:
            diff[zonetab.distance(lat, lon, row['latitude'], row['longitude'])] = row['id']
        self.gclose()
        keys = list(diff.keys())
        keys.sort()

        dict = {}
        if keys == []:
            dict = {'country': None, 'admin1': None, 'geonameid': None, 'continent': None, 'timezonestr': None}
            dprint('gnearest: no town found within 66km range!')
        else:
            sql = 'SELECT * FROM geonames WHERE id=%s LIMIT 1' % (diff[keys[0]])
            self.gquery(sql)
            geoname = self.gcursor.fetchone()
            self.gclose()
            dict['country'] = geoname['country']
            dict['admin1'] = geoname['admin1']
            dict['geonameid'] = geoname['geonameid']
            dict['timezonestr'] = geoname['timezone']
            sql = 'SELECT * FROM countryinfo WHERE isoalpha2="%s" LIMIT 1' % (geoname['country'])
            self.gquery(sql)
            countryinfo = self.gcursor.fetchone()
            dict['continent'] = countryinfo['continent']
            self.gclose()
            dprint('gnearest: found town %s at %s,%s,%s' % (geoname['name'], geoname['latitude'],
                                                            geoname['longitude'], geoname['timezone']))
        return dict

    def gquery(self, sql, tuple=None):
        self.glink = sqlite3.connect(cfg.geonamesdb)
        self.glink.row_factory = sqlite3.Row
        self.gcursor = self.glink.cursor()
        if tuple:
            self.gcursor.execute(sql, tuple)
        else:
            self.gcursor.execute(sql)

    def gclose(self):
        self.glink.commit()
        self.gcursor.close()
        self.glink.close()

    def open(self):
        self.link = sqlite3.connect(cfg.astrodb)
        self.link.row_factory = sqlite3.Row
        self.cursor = self.link.cursor()

        # self.plink = sqlite3.connect(cfg.peopledb)
        # self.plink.row_factory = sqlite3.Row
        # self.pcursor = self.plink.cursor()

    def close(self):
        self.cursor.close()
        # self.pcursor.close()
        # self.link.close()
        # self.plink.close()


# db = openAstroSqlite()

# calculation and svg drawing class

class openAstroInstance:

    def __init__(self, selection):
        self.db = openAstroSqlite()
        self.label = self.db.getLabel()

        self.selection = selection
        self.astrocfg = None
        self.set_astrocfg(selection)

        self.location = selection['location']
        self.geolat = selection['geolat']
        self.geolon = selection['geolon']
        self.countrycode = selection['countrycode']
        self.timezonestr = selection['timezonestr']

        # current datetime
        date = selection['date']

        # aware datetime object
        dt_input = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second)
        dt = pytz.timezone(self.timezonestr).localize(dt_input)

        # naive utc datetime object
        dt_utc = dt.replace(tzinfo=None) - dt.utcoffset()

        dt_utc = date.astimezone(pytz.utc)
        # Default
        # self.name = "Here and Now")
        # self.charttype = self.label["radix"]
        self.year = dt_utc.year
        self.month = dt_utc.month
        self.day = dt_utc.day
        self.hour = self.decHourJoin(dt_utc.hour, dt_utc.minute, dt_utc.second)

        self.str_date_utc = dt_utc.strftime(DATE_FORMAT)

        self.timezone = self.offsetToTz(dt.utcoffset())
        self.altitude = selection['altitude']
        self.geonameid = None

        # Make locals
        self.utcToLocal()

        # get color configuration
        self.colors = self.db.getColors()

        # configuration
        # ZOOM 1 = 100%
        self.zoom = 1
        self.type = "Transit" if selection['transit_date'] else "Radix"

        if self.type == "Transit":
            self.t_geolon = float(self.geolon)
            self.t_geolat = float(self.geolat)

            now = datetime.datetime.now()
            timezone_str = zonetab.nearest_tz(self.t_geolat, self.t_geolon, zonetab.timezones())[2]
            # aware datetime object
            transit_date = selection['transit_date']
            dt_utc = transit_date.astimezone(pytz.utc)

            # dt_input = datetime.datetime(
            #     transit_date.year,
            #     transit_date.month,
            #     transit_date.day,
            #     transit_date.hour,
            #     transit_date.minute,
            #     transit_date.second,
            # )
            # dt = pytz.timezone(timezone_str).localize(dt_input)
            # # naive utc datetime object
            # dt_utc = dt.replace(tzinfo=None) - dt.utcoffset()
            # transit data
            self.t_year = dt_utc.year
            self.t_month = dt_utc.month
            self.t_day = dt_utc.day
            self.t_hour = self.decHourJoin(dt_utc.hour, dt_utc.minute, dt_utc.second)
            # self.t_timezone = self.offsetToTz(dt.utcoffset())
            self.t_altitude = self.altitude

        # 12 zodiacs
        self.zodiac = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius',
                       'capricorn', 'aquarius', 'pisces']
        self.zodiac_short = ['Ari', 'Tau', 'Gem', 'Cnc', 'Leo', 'Vir', 'Lib', 'Sco', 'Sgr', 'Cap', 'Aqr', 'Psc']
        self.zodiac_color = ['#482900', '#6b3d00', '#5995e7', '#2b4972', '#c54100', '#2b286f', '#69acf1', '#ffd237',
                             '#ff7200', '#863c00', '#4f0377', '#6cbfff']
        self.zodiac_element = ['fire', 'earth', 'air', 'water', 'fire', 'earth', 'air', 'water', 'fire', 'earth', 'air',
                               'water']

        # get color configuration
        # self.colors = self.db.getColors()

        self.siderealmode_chartview = {
            "FAGAN_BRADLEY": "Fagan Bradley",
            "LAHIRI": "Lahiri",
            "DELUCE": "Deluce",
            "RAMAN": "Ramanb",
            "USHASHASHI": "Ushashashi",
            "KRISHNAMURTI": "Krishnamurti",
            "DJWHAL_KHUL": "Djwhal Khul",
            "YUKTESHWAR": "Yukteshwar",
            "JN_BHASIN": "Jn Bhasin",
            "BABYL_KUGLER1": "Babyl Kugler 1",
            "BABYL_KUGLER2": "Babyl Kugler 2",
            "BABYL_KUGLER3": "Babyl Kugler 3",
            "BABYL_HUBER": "Babyl Huber",
            "BABYL_ETPSC": "Babyl Etpsc",
            "ALDEBARAN_15TAU": "Aldebaran 15Tau",
            "HIPPARCHOS": "Hipparchos",
            "SASSANIAN": "Sassanian",
            "J2000": "J2000",
            "J1900": "J1900",
            "B1950": "B1950",
        }

        self.load()

    def set_astrocfg(self, selection):

        self.astrocfg = copy.deepcopy(
            self.db.astrocfg,
        )

        for key in selection.keys():
            if key in self.astrocfg:
                self.astrocfg[key] = selection[key]
        self.astrocfg["houses_system"] = selection["houses_system"]
        self.astrocfg["siderealmode"] = selection["sidereal_mode"]

    def get_calculation_methods(self):
        return {
            "geo": self.label["apparent_geocentric"],
            "truegeo": self.label["true_geocentric"],
            "topo": self.label["topocentric"],
            "helio": self.label["heliocentric"],
        }

    def get_houses_system(self):
        return {
            "P": "Placidus",
            "K": "Koch",
            "O": "Porphyrius",
            "R": "Regiomontanus",
            "C": "Campanus",
            "A": "Equal (Cusp 1 = Asc)",
            "V": "Vehlow Equal (Asc = 1/2 House 1)",
            "W": "Whole",
            "X": "Axial Rotation",
            "H": "Azimuthal or Horizontal System",
            "T": "Polich/Page ('topocentric system')",
            "B": "Alcabitus",
            "G": "Gauquelin sectors",
            "M": "Morinus"
        }

    def get_houses_system_code(self, name):
        data = {
            "Placidus": "P",
            "Koch": "K",
            "Porphyrius": "O",
            "Regiomontanus": "R",
            "Campanus": "C",
            "Equal (Cusp 1 = Asc)": "A",
            "Vehlow Equal (Asc = 1/2 House 1)": "V",
            "Whole": "W",
            "Axial Rotation": "X",
            "Azimuthal or Horizontal System": "H",
            "Polich/Page ('topocentric system')": "T",
            "Alcabitus": "B",
            "Gauquelin sectors": "G",
            "Morinus": "M",
        }
        return data[name] if name in data.keys() else ""

    def get_sidereal_modes(self):
        return self.siderealmode_chartview

    def utcToLocal(self):
        # make local time variables from global UTC
        h, m, s = self.decHour(self.hour)
        utc = datetime.datetime(self.year, self.month, self.day, h, m, s)
        tz = datetime.timedelta(seconds=float(self.timezone) * float(3600))
        loc = utc + tz
        self.year_loc = loc.year
        self.month_loc = loc.month
        self.day_loc = loc.day
        self.hour_loc = loc.hour
        self.minute_loc = loc.minute
        self.second_loc = loc.second
        # print some info
        dprint('utcToLocal: ' + str(utc) + ' => ' + str(loc) + self.decTzStr(self.timezone))

    def localToSolar(self, newyear):
        solaryearsecs = 31556925.51  # 365 days, 5 hours, 48 minutes, 45.51 seconds
        dprint("localToSolar: from %s to %s" % (self.year, newyear))
        h, m, s = self.decHour(self.hour)
        dt_original = datetime.datetime(self.year, self.month, self.day, h, m, s)
        dt_new = datetime.datetime(newyear, self.month, self.day, h, m, s)
        dprint("localToSolar: first sun %s" % (self.planets_degree_ut[0]))
        mdata = ephemeris.ephData(newyear, self.month, self.day, self.hour, self.geolon, self.geolat, self.altitude,
                                  self.planets, self.zodiac, self.astrocfg)
        dprint("localToSolar: second sun %s" % (mdata.planets_degree_ut[0]))
        sundiff = self.planets_degree_ut[0] - mdata.planets_degree_ut[0]
        dprint("localToSolar: sundiff %s" % (sundiff))
        sundelta = (sundiff / 360.0) * solaryearsecs
        dprint("localToSolar: sundelta %s" % (sundelta))
        dt_delta = datetime.timedelta(seconds=int(sundelta))
        dt_new = dt_new + dt_delta
        mdata = ephemeris.ephData(dt_new.year, dt_new.month, dt_new.day,
                                  self.decHourJoin(dt_new.hour, dt_new.minute, dt_new.second), self.geolon, self.geolat,
                                  self.altitude, self.planets, self.zodiac, self.astrocfg)
        dprint("localToSolar: new sun %s" % (mdata.planets_degree_ut[0]))

        # get precise
        step = 0.000011408  # 1 seconds in degrees
        sundiff = self.planets_degree_ut[0] - mdata.planets_degree_ut[0]
        sundelta = sundiff / step
        dt_delta = datetime.timedelta(seconds=int(sundelta))
        dt_new = dt_new + dt_delta
        mdata = ephemeris.ephData(dt_new.year, dt_new.month, dt_new.day,
                                  self.decHourJoin(dt_new.hour, dt_new.minute, dt_new.second), self.geolon, self.geolat,
                                  self.altitude, self.planets, self.zodiac, self.astrocfg)
        dprint("localToSolar: new sun #2 %s" % (mdata.planets_degree_ut[0]))

        step = 0.000000011408  # 1 milli seconds in degrees
        sundiff = self.planets_degree_ut[0] - mdata.planets_degree_ut[0]
        sundelta = sundiff / step
        dt_delta = datetime.timedelta(milliseconds=int(sundelta))
        dt_new = dt_new + dt_delta
        mdata = ephemeris.ephData(dt_new.year, dt_new.month, dt_new.day,
                                  self.decHourJoin(dt_new.hour, dt_new.minute, dt_new.second), self.geolon, self.geolat,
                                  self.altitude, self.planets, self.zodiac, self.astrocfg)
        dprint("localToSolar: new sun #3 %s" % (mdata.planets_degree_ut[0]))

        self.s_year = dt_new.year
        self.s_month = dt_new.month
        self.s_day = dt_new.day
        self.s_hour = self.decHourJoin(dt_new.hour, dt_new.minute, dt_new.second)
        self.s_geolon = self.geolon
        self.s_geolat = self.geolat
        self.s_altitude = self.altitude
        self.type = "Solar"
        openAstro.charttype = "%s (%s-%02d-%02d %02d:%02d:%02d UTC)" % (
        openAstro.label["solar"], self.s_year, self.s_month, self.s_day, dt_new.hour, dt_new.minute, dt_new.second)
        openAstro.transit = False
        return

    def localToSecondaryProgression(self, dt):

        # remove timezone
        dt_utc = dt - datetime.timedelta(seconds=float(self.timezone) * float(3600))
        h, m, s = self.decHour(self.hour)
        dt_new = ephemeris.years_diff(self.year, self.month, self.day, self.hour,
                                      dt_utc.year, dt_utc.month, dt_utc.day, self.decHourJoin(dt_utc.hour,
                                                                                              dt_utc.minute,
                                                                                              dt_utc.second))

        self.sp_year = dt_new.year
        self.sp_month = dt_new.month
        self.sp_day = dt_new.day
        self.sp_hour = self.decHourJoin(dt_new.hour, dt_new.minute, dt_new.second)
        self.sp_geolon = self.geolon
        self.sp_geolat = self.geolat
        self.sp_altitude = self.altitude
        self.houses_override = [dt_new.year, dt_new.month, dt_new.day, self.hour]

        dprint("localToSecondaryProgression: got UTC %s-%s-%s %s:%s:%s" % (
            dt_new.year, dt_new.month, dt_new.day, dt_new.hour, dt_new.minute, dt_new.second))

        self.type = "SecondaryProgression"
        openAstro.charttype = "%s (%s-%02d-%02d %02d:%02d)" % (
        openAstro.label["secondary_progressions"], dt.year, dt.month, dt.day, dt.hour, dt.minute)
        openAstro.transit = False
        return

    def load(self):
        # empty element points
        self.fire = 0.0
        self.earth = 0.0
        self.air = 0.0
        self.water = 0.0

        astrocfg_keys = self.db.astrocfg.keys()

        # get database planet settings
        self.planets = self.db.getSettingsPlanet()

        # get database aspect settings
        self.aspects = self.db.getSettingsAspect()

        # Combine module data
        if self.type == "Combine":
            # make calculations
            module_data = ephemeris.ephData(self.c_year, self.c_month, self.c_day, self.c_hour, self.c_geolon,
                                            self.c_geolat, self.c_altitude, self.planets, self.zodiac, self.astrocfg)

        # Solar module data
        if self.type == "Solar":
            module_data = ephemeris.ephData(self.s_year, self.s_month, self.s_day, self.s_hour, self.s_geolon,
                                            self.s_geolat, self.s_altitude, self.planets, self.zodiac, self.astrocfg)

        elif self.type == "SecondaryProgression":
            module_data = ephemeris.ephData(self.sp_year, self.sp_month, self.sp_day, self.sp_hour, self.sp_geolon,
                                            self.sp_geolat, self.sp_altitude, self.planets, self.zodiac, self.astrocfg,
                                            houses_override=self.houses_override)

        elif self.type == "Transit" or self.type == "Composite":
            module_data = ephemeris.ephData(self.year, self.month, self.day, self.hour, self.geolon, self.geolat,
                                            self.altitude, self.planets, self.zodiac, self.astrocfg)
            t_module_data = ephemeris.ephData(self.t_year, self.t_month, self.t_day, self.t_hour, self.t_geolon,
                                              self.t_geolat, self.t_altitude, self.planets, self.zodiac, self.astrocfg)

        else:
            # make calculations
            module_data = ephemeris.ephData(self.year, self.month, self.day, self.hour, self.geolon, self.geolat,
                                            self.altitude, self.planets, self.zodiac, self.astrocfg)

        # Transit module data
        if self.type == "Transit" or self.type == "Composite":
            # grab transiting module data
            self.t_planets_sign = t_module_data.planets_sign
            self.t_planets_degree = t_module_data.planets_degree
            self.t_planets_degree_ut = t_module_data.planets_degree_ut
            self.t_planets_retrograde = t_module_data.planets_retrograde
            self.t_houses_degree = t_module_data.houses_degree
            self.t_houses_sign = t_module_data.houses_sign
            self.t_houses_degree_ut = t_module_data.houses_degree_ut

        # grab normal module data
        self.planets_sign = module_data.planets_sign
        self.planets_degree = module_data.planets_degree
        self.planets_degree_ut = module_data.planets_degree_ut
        self.planets_retrograde = module_data.planets_retrograde
        self.houses_degree = module_data.houses_degree
        self.houses_sign = module_data.houses_sign
        self.houses_degree_ut = module_data.houses_degree_ut
        self.lunar_phase = module_data.lunar_phase

        print("DEBUG / openAstroInstance / load / db.astrocfg['zodiactype'] = {}".format(self.astrocfg["zodiactype"]))
        print("DEBUG / openAstroInstance / load / self.houses_degree_ut = {}".format(self.houses_degree_ut))

        # make composite averages
        if self.type == "Composite":
            # new houses
            asc = self.houses_degree_ut[0]
            t_asc = self.t_houses_degree_ut[0]
            for i in range(12):
                # difference in distances measured from ASC
                diff = self.houses_degree_ut[i] - asc
                if diff < 0:
                    diff = diff + 360.0
                t_diff = self.t_houses_degree_ut[i] - t_asc
                if t_diff < 0:
                    t_diff = t_diff + 360.0
                newdiff = (diff + t_diff) / 2.0

                # new ascendant
                if asc > t_asc:
                    diff = asc - t_asc
                    if diff > 180:
                        diff = 360.0 - diff
                        nasc = asc + (diff / 2.0)
                    else:
                        nasc = t_asc + (diff / 2.0)
                else:
                    diff = t_asc - asc
                    if diff > 180:
                        diff = 360.0 - diff
                        nasc = t_asc + (diff / 2.0)
                    else:
                        nasc = asc + (diff / 2.0)

                # new house degrees
                self.houses_degree_ut[i] = nasc + newdiff
                if self.houses_degree_ut[i] > 360:
                    self.houses_degree_ut[i] = self.houses_degree_ut[i] - 360.0

                # new house sign
                for x in range(len(self.zodiac)):
                    deg_low = float(x * 30)
                    deg_high = float((x + 1) * 30)
                    if self.houses_degree_ut[i] >= deg_low:
                        if self.houses_degree_ut[i] <= deg_high:
                            self.houses_sign[i] = x
                            self.houses_degree[i] = self.houses_degree_ut[i] - deg_low

            # new planets
            for i in range(23):
                # difference in degrees
                p1 = self.planets_degree_ut[i]
                p2 = self.t_planets_degree_ut[i]
                if p1 > p2:
                    diff = p1 - p2
                    if diff > 180:
                        diff = 360.0 - diff
                        self.planets_degree_ut[i] = (diff / 2.0) + p1
                    else:
                        self.planets_degree_ut[i] = (diff / 2.0) + p2
                else:
                    diff = p2 - p1
                    if diff > 180:
                        diff = 360.0 - diff
                        self.planets_degree_ut[i] = (diff / 2.0) + p2
                    else:
                        self.planets_degree_ut[i] = (diff / 2.0) + p1

                if self.planets_degree_ut[i] > 360:
                    self.planets_degree_ut[i] = self.planets_degree_ut[i] - 360.0

            # list index 23 is asc, 24 is Mc, 25 is Dsc, 26 is Ic
            self.planets_degree_ut[23] = self.houses_degree_ut[0]
            self.planets_degree_ut[24] = self.houses_degree_ut[9]
            self.planets_degree_ut[25] = self.houses_degree_ut[6]
            self.planets_degree_ut[26] = self.houses_degree_ut[3]

            # new planet signs
            for i in range(27):
                for x in range(len(self.zodiac)):
                    deg_low = float(x * 30)
                    deg_high = float((x + 1) * 30)
                    if self.planets_degree_ut[i] >= deg_low:
                        if self.planets_degree_ut[i] <= deg_high:
                            self.planets_sign[i] = x
                            self.planets_degree[i] = self.planets_degree_ut[i] - deg_low
                            self.planets_retrograde[i] = False

        # template dictionary
        td = dict()
        r = 240
        if (self.astrocfg['chartview'] == "european"):
            self.c1 = 56
            self.c2 = 92
            self.c3 = 112
        else:
            self.c1 = 0
            self.c2 = 36
            self.c3 = 120

        # bottom left
        # siderealmode_chartview={
        # 		"FAGAN_BRADLEY":"Fagan Bradley",
        # 		"LAHIRI":"Lahiri",
        # 		"DELUCE":"Deluce",
        # 		"RAMAN":"Ramanb",
        # 		"USHASHASHI":"Ushashashi",
        # 		"KRISHNAMURTI":"Krishnamurti",
        # 		"DJWHAL_KHUL":"Djwhal Khul",
        # 		"YUKTESHWAR":"Yukteshwar",
        # 		"JN_BHASIN":"Jn Bhasin",
        # 		"BABYL_KUGLER1":"Babyl Kugler 1",
        # 		"BABYL_KUGLER2":"Babyl Kugler 2",
        # 		"BABYL_KUGLER3":"Babyl Kugler 3",
        # 		"BABYL_HUBER":"Babyl Huber",
        # 		"BABYL_ETPSC":"Babyl Etpsc",
        # 		"ALDEBARAN_15TAU":"Aldebaran 15Tau",
        # 		"HIPPARCHOS":"Hipparchos",
        # 		"SASSANIAN":"Sassanian",
        # 		"J2000":"J2000",
        # 		"J1900":"J1900",
        # 		"B1950":"B1950")
        # 		}

        # lunar phase
        deg = self.lunar_phase['degrees']

        if (deg < 90.0):
            maxr = deg
            if (deg > 80.0): maxr = maxr * maxr
            lfcx = 20.0 + (deg / 90.0) * (maxr + 10.0)
            lfr = 10.0 + (deg / 90.0) * maxr
            lffg, lfbg = self.colors["lunar_phase_0"], self.colors["lunar_phase_1"]

        elif (deg < 180.0):
            maxr = 180.0 - deg
            if (deg < 100.0): maxr = maxr * maxr
            lfcx = 20.0 + ((deg - 90.0) / 90.0 * (maxr + 10.0)) - (maxr + 10.0)
            lfr = 10.0 + maxr - ((deg - 90.0) / 90.0 * maxr)
            lffg, lfbg = self.colors["lunar_phase_1"], self.colors["lunar_phase_0"]

        elif (deg < 270.0):
            maxr = deg - 180.0
            if (deg > 260.0): maxr = maxr * maxr
            lfcx = 20.0 + ((deg - 180.0) / 90.0 * (maxr + 10.0))
            lfr = 10.0 + ((deg - 180.0) / 90.0 * maxr)
            lffg, lfbg = self.colors["lunar_phase_1"], self.colors["lunar_phase_0"]

        elif (deg < 361):
            maxr = 360.0 - deg
            if (deg < 280.0): maxr = maxr * maxr
            lfcx = 20.0 + ((deg - 270.0) / 90.0 * (maxr + 10.0)) - (maxr + 10.0)
            lfr = 10.0 + maxr - ((deg - 270.0) / 90.0 * maxr)
            lffg, lfbg = self.colors["lunar_phase_0"], self.colors["lunar_phase_1"]

        # #read template
        # f=open(cfg.xml_svg)
        # template=Template(f.read()).substitute(td)
        # f.close()
        #
        # #write template
        # if printing:
        # 	f=open(cfg.tempfilenameprint,"w")
        # 	dprint("Printing SVG: lat="+str(self.geolat)+' lon='+str(self.geolon)+' loc='+self.location)
        # else:
        # 	f=open(cfg.tempfilename,"w")
        # 	dprint("Creating SVG: lat="+str(self.geolat)+' lon='+str(self.geolon)+' loc='+self.location)
        #
        # f.write(template)
        # f.close()
        #
        # #return filename
        # return cfg.tempfilename

    def get_houses_degree_ut(self):
        return self.houses_degree_ut

    def get_conjunctions(self, aspects):
        conjunctions = []
        for aspect in aspects:
            if aspect['aspect']['name'] == "conjunction":
                planet1 = aspect['planets'][0]['name']
                planet2 = aspect['planets'][1]['name']
                if planet1 in PLANETS_OF_INTEREST and planet2 in PLANETS_OF_INTEREST:
                    conjunctions.append(
                        "{} - {}".format(
                            planet1.capitalize(),
                            planet2.capitalize(),
                        )
                    )
        return conjunctions

    def get_data(self):

        transit = dict(
            planets=None,
            zodiac=None,
            houses=None,
            aspects=None
        )
        houses = self.makeHouses()
        zodiac = self.makeZodiac()
        planets, t_planets = self.makePlanets()

        print("=========================== report ======================================")
        print("date : {}".format(self.selection['date']))
        print("houses : {}".format(houses))
        print("zodiac : {}".format(zodiac))
        for key in planets.keys():
            print("{} : {}".format(key, planets[key]))
        print("=========================== report ======================================")

        if "european" == self.astrocfg['chartview']:
            # self.c1=56
            # self.c2=92
            c3 = 112
        else:
            # self.c1=0
            # self.c2=36
            c3 = 120
        r = 240
        aspects = self.makeAspects(r, ar=(r - c3))

        if self.type == "Transit":
            t_houses = self.makeHousesTransit()
            t_aspects = self.makeAspectsTransit()
            transit.update(
                dict(
                    planets=t_planets,
                    zodiac=zodiac,
                    houses=t_houses,
                    aspects=t_aspects,
                ),
            )

        houses_system = list(self.get_houses_system().values())
        selected_houses_system = self.get_houses_system()[self.astrocfg['houses_system']]
        houses_system_index = houses_system.index(selected_houses_system)

        data = {
            'houses': houses,
            'zodiac': zodiac,
            'planets': planets,
            'transit': transit,
            "aspects": aspects,
            "conjunctions": self.get_conjunctions(aspects),
            'selection': {
                'zodiactype': self.selection['zodiactype'],
                'location': self.location,
                'countrycode': self.countrycode,
                'timezone': self.timezonestr,
                "date": self.str_date_utc,
                'latitude': self.geolat,
                'longitude': self.geolon,
                'houses_system': houses_system,
                'houses_system_index': houses_system_index,
                "chartview": self.astrocfg['chartview'],
            },
            'settings': {
                "houses_system": houses_system,
                'calculation_methods': list(self.get_calculation_methods().values())

            },
        }

        if self.selection['zodiactype'] == 'sidereal':

            sidereal_modes = list(
                self.get_sidereal_modes().values(),
            )
            sidereal_mode = self.get_sidereal_modes()[self.astrocfg['siderealmode']]
            sidereal_mode_index = sidereal_modes.index(sidereal_mode)

            data['selection']['sidereal_modes'] = sidereal_modes
            data['selection']['sidereal_mode_index'] = sidereal_mode_index

            data['settings']['sidereal_modes'] = sidereal_modes

        return data

    def get_elongation(self, angle):
        zodiac = self.makeZodiac()
        zodiac_angles = zodiac['angles']
        zodiac_labels = zodiac['labels']

        zodiac_angles = numpy.array(zodiac_angles) % 360
        zodiac_labels = numpy.array(zodiac_labels)

        sorted_indices = numpy.argsort(zodiac_angles)

        angles = zodiac_angles[sorted_indices]
        dangles = angle - angles
        positive = dangles >= 0

        if len(dangles[positive]) == 0:
            dangles = angle + 360 - angles
            positive = dangles >= 0

        elongation_index = numpy.argmin(dangles[positive])
        elongation = dangles[positive][elongation_index]
        zodiac_label = zodiac_labels[sorted_indices[positive][elongation_index]]
        label_degree_minutes_seconds = convert_degrees_minutes_seconds(elongation)
        angle_degree_minutes = convert_degrees_minutes(elongation)

        label_degrees = "{}°".format(
            int(
                round(elongation),
            ),
        )

        return label_degrees, angle_degree_minutes, label_degree_minutes_seconds, zodiac_label

    # draw transit ring
    def transitRing(self, r):
        out = '<circle cx="%s" cy="%s" r="%s" style="fill: none; stroke: %s; stroke-width: 36px; stroke-opacity: .4;"/>' % (
        r, r, r - 18, self.colors['paper_1'])
        out += '<circle cx="%s" cy="%s" r="%s" style="fill: none; stroke: %s; stroke-width: 1px; stroke-opacity: .6;"/>' % (
        r, r, r, self.colors['zodiac_transit_ring_3'])
        return out

    # draw degree ring
    def degreeRing(self, r):
        out = ''
        for i in range(72):
            offset = float(i * 5) - self.houses_degree_ut[6]
            if offset < 0:
                offset = offset + 360.0
            elif offset > 360:
                offset = offset - 360.0
            x1 = self.sliceToX(0, r - self.c1, offset) + self.c1
            y1 = self.sliceToY(0, r - self.c1, offset) + self.c1
            x2 = self.sliceToX(0, r + 2 - self.c1, offset) - 2 + self.c1
            y2 = self.sliceToY(0, r + 2 - self.c1, offset) - 2 + self.c1
            out += '<line x1="%s" y1="%s" x2="%s" y2="%s" style="stroke: %s; stroke-width: 1px; stroke-opacity:.9;"/>\n' % (
                x1, y1, x2, y2, self.colors['paper_0'])
        return out

    def degreeTransitRing(self, r):
        out = ''
        for i in range(72):
            offset = float(i * 5) - self.houses_degree_ut[6]
            if offset < 0:
                offset = offset + 360.0
            elif offset > 360:
                offset = offset - 360.0
            x1 = self.sliceToX(0, r, offset)
            y1 = self.sliceToY(0, r, offset)
            x2 = self.sliceToX(0, r + 2, offset) - 2
            y2 = self.sliceToY(0, r + 2, offset) - 2
            out += '<line x1="%s" y1="%s" x2="%s" y2="%s" style="stroke: #F00; stroke-width: 1px; stroke-opacity:.9;"/>\n' % (
                x1, y1, x2, y2)
        return out

    # floating latitude an longitude to string
    def lat2str(self, coord):
        sign = self.label["north"]
        if coord < 0.0:
            sign = self.label["south"]
            coord = abs(coord)
        deg = int(coord)
        min = int((float(coord) - deg) * 60)
        sec = int(round(float(((float(coord) - deg) * 60) - min) * 60.0))
        return "%s°%s'%s\" %s" % (deg, min, sec, sign)

    def lon2str(self, coord):
        sign = self.label["east"]
        if coord < 0.0:
            sign = self.label["west"]
            coord = abs(coord)
        deg = int(coord)
        min = int((float(coord) - deg) * 60)
        sec = int(round(float(((float(coord) - deg) * 60) - min) * 60.0))
        return "%s°%s'%s\" %s" % (deg, min, sec, sign)

    # decimal hour to minutes and seconds
    def decHour(self, input):
        hours = int(input)
        mands = (input - hours) * 60.0
        mands = round(mands, 5)
        minutes = int(mands)
        seconds = int(round((mands - minutes) * 60))
        return [hours, minutes, seconds]

    # join hour, minutes, seconds, timezone integere to hour float
    def decHourJoin(self, inH, inM, inS):
        dh = float(inH)
        dm = float(inM) / 60
        ds = float(inS) / 3600
        output = dh + dm + ds
        return output

    # Datetime offset to float in hours
    def offsetToTz(self, dtoffset):
        dh = float(dtoffset.days * 24)
        sh = float(dtoffset.seconds / 3600.0)
        output = dh + sh
        return output

    # decimal timezone string
    def decTzStr(self, tz):
        if tz > 0:
            h = int(tz)
            m = int((float(tz) - float(h)) * float(60))
            return " [+%(#1)02d:%(#2)02d]" % {'#1': h, '#2': m}
        else:
            h = int(tz)
            m = int((float(tz) - float(h)) * float(60)) / -1
            return " [-%(#1)02d:%(#2)02d]" % {'#1': h / -1, '#2': m}

    # degree difference
    def degreeDiff(self, a, b):
        out = float()
        if a > b:
            out = a - b
        if a < b:
            out = b - a
        if out > 180.0:
            out = 360.0 - out
        return out

    # decimal to degrees (a°b'c")
    def dec2deg(self, dec, type="3"):
        dec = float(dec)
        a = int(dec)
        a_new = (dec - float(a)) * 60.0
        b_rounded = int(round(a_new))
        b = int(a_new)
        c = int(round((a_new - float(b)) * 60.0))
        if type == "3":
            out = '%(#1)02d&#176;%(#2)02d&#39;%(#3)02d&#34;' % {'#1': a, '#2': b, '#3': c}
        elif type == "2":
            out = '%(#1)02d&#176;%(#2)02d&#39;' % {'#1': a, '#2': b_rounded}
        elif type == "1":
            out = '%(#1)02d&#176;' % {'#1': a}
        return str(out)

    # draw svg aspects: ring, aspect ring, degreeA degreeB
    def drawAspect(self, r, ar, degA, degB, color):
        offset = (int(self.houses_degree_ut[6]) / -1) + int(degA)
        x1 = self.sliceToX(0, ar, offset) + (r - ar)
        y1 = self.sliceToY(0, ar, offset) + (r - ar)
        offset = (int(self.houses_degree_ut[6]) / -1) + int(degB)
        x2 = self.sliceToX(0, ar, offset) + (r - ar)
        y2 = self.sliceToY(0, ar, offset) + (r - ar)
        out = '			<line x1="' + str(x1) + '" y1="' + str(y1) + '" x2="' + str(x2) + '" y2="' + str(
            y2) + '" style="stroke: ' + color + '; stroke-width: 1; stroke-opacity: .9;"/>\n'
        return out

    def sliceToX(self, slice, r, offset):
        plus = (math.pi * offset) / 180
        radial = ((math.pi / 6) * slice) + plus
        return r * (math.cos(radial) + 1)

    def sliceToY(self, slice, r, offset):
        plus = (math.pi * offset) / 180
        radial = ((math.pi / 6) * slice) + plus
        return r * ((math.sin(radial) / -1) + 1)

    def zodiacSlice(self, num, r, style, type):
        # pie slices
        if self.astrocfg["houses_system"] == "G":
            offset = 360 - self.houses_degree_ut[18]
        else:
            offset = 360 - self.houses_degree_ut[6]
        # check transit
        if self.type == "Transit":
            dropin = 0
        else:
            dropin = self.c1
        slice = '<path d="M' + str(r) + ',' + str(r) + ' L' + str(
            dropin + self.sliceToX(num, r - dropin, offset)) + ',' + str(
            dropin + self.sliceToY(num, r - dropin, offset)) + ' A' + str(r - dropin) + ',' + str(
            r - dropin) + ' 0 0,0 ' + str(dropin + self.sliceToX(num + 1, r - dropin, offset)) + ',' + str(
            dropin + self.sliceToY(num + 1, r - dropin, offset)) + ' z" style="' + style + '"/>'
        # symbols
        offset = offset + 15
        # check transit
        if self.type == "Transit":
            dropin = 54
        else:
            dropin = 18 + self.c1
        sign = '<g transform="translate(-16,-16)"><use x="' + str(
            dropin + self.sliceToX(num, r - dropin, offset)) + '" y="' + str(
            dropin + self.sliceToY(num, r - dropin, offset)) + '" xlink:href="#' + type + '" /></g>\n'
        return slice + '\n' + sign

    # def makeZodiac(self, r=240):
    #     output = ""
    #     for i in range(len(self.zodiac)):
    #         output = output + self.zodiacSlice(i, r,
    #                                            "fill:" + self.colors["zodiac_bg_%s" % (i)] + "; fill-opacity: 0.5;",
    #                                            self.zodiac[i]) + '\n'
    #     return output

    def makeHouses(self, r=240):
        path = ""
        offsets = []
        if self.astrocfg["houses_system"] == "G":
            xr = 36
        else:
            xr = 12
        for i in range(xr):
            # offset is negative desc houses_degree_ut[6]
            offset = (int(self.houses_degree_ut[int(xr / 2)]) / -1) + int(self.houses_degree_ut[i])
            offsets.append(offset)

        houses_degree_ut = numpy.array(self.houses_degree_ut)
        res = houses_degree_ut - houses_degree_ut[int(xr / 2)]
        print("DEBUG / openAstroInstance / makeHouses / self.houses_degree_ut = {}".format(self.houses_degree_ut))
        print("DEBUG / openAstroInstance / makeHouses / res = {}".format(res))
        # wres = res + 360
        # return wres % 360
        wres = res + 360
        wres = wres % 360
        wres.round()
        labels = numpy.array(list(HOUSES_ICONS.keys()))
        sorted_indexes = numpy.argsort(wres)
        return {'angles': wres[sorted_indexes].tolist(), 'labels': labels[sorted_indexes].tolist()}

    def makeHousesTransit(self, r=240):
        offsets = []
        if self.astrocfg["houses_system"] == "G":
            xr = 36
        else:
            xr = 12
        zeropoint = 360 - self.houses_degree_ut[6]
        for i in range(xr):
            # offset is negative desc houses_degree_ut[6]
            offset = zeropoint + self.t_houses_degree_ut[i]
            if offset > 360:
                offset -= 360
            if i < 11:
                offset += int(self.degreeDiff(self.t_houses_degree_ut[(i + 1)], self.t_houses_degree_ut[i]) / 2)
            else:
                offset += int(self.degreeDiff(self.t_houses_degree_ut[0], self.t_houses_degree_ut[11]) / 2)
            # if offset > 360:
            #     offset = offset - 360
            offsets.append(offset)

        res = numpy.array(offsets)

        wres = res + 360
        wres = wres % 360
        wres.round()
        labels = numpy.array(list(HOUSES_ICONS.keys()))
        sorted_indexes = numpy.argsort(wres)
        return {'angles': wres[sorted_indexes].tolist(), 'labels': labels[sorted_indexes].tolist()}

    def makeZodiac(self):
        # pie slices
        if self.astrocfg["houses_system"] == "G":
            offset = 360 - self.houses_degree_ut[18]
        else:
            offset = 360 - self.houses_degree_ut[6]

        res = (offset + numpy.array([30 * i for i in range(12)])) % 360
        labels = numpy.array(
            self.zodiac,
        )
        sorted_indexes = numpy.argsort(res)
        return {'angles': res[sorted_indexes].tolist(), 'labels': labels[sorted_indexes].tolist()}

    def makePlanets(self, r=240):

        planets_degut = {}

        diff = range(len(self.planets))
        for i in range(len(self.planets)):
            # if self.planets[i]['visible'] == 1:
            if True:
                # list of planets sorted by degree
                planets_degut[self.planets_degree_ut[i]] = i

            # element: get extra points if planet is in own zodiac
            pz = self.planets[i]['zodiac_relation']
            cz = self.planets_sign[i]
            extrapoints = 0
            if pz != -1:
                for e in range(len(pz.split(','))):
                    if int(pz.split(',')[e]) == int(cz):
                        extrapoints = 10

            # calculate element points for all planets
            ele = self.zodiac_element[self.planets_sign[i]]
            if ele == "fire":
                self.fire = self.fire + self.planets[i]['element_points'] + extrapoints
            elif ele == "earth":
                self.earth = self.earth + self.planets[i]['element_points'] + extrapoints
            elif ele == "air":
                self.air = self.air + self.planets[i]['element_points'] + extrapoints
            elif ele == "water":
                self.water = self.water + self.planets[i]['element_points'] + extrapoints

        output = ""
        keys = list(planets_degut.keys())
        keys.sort()
        switch = 0

        planets_degrouped = {}
        groups = []
        planets_by_pos = list(range(len(planets_degut)))
        planet_drange = 3.4
        # get groups closely together
        group_open = False
        for e in range(len(keys)):
            i = planets_degut[keys[e]]
            # get distances between planets
            if e == 0:
                prev = self.planets_degree_ut[planets_degut[keys[-1]]]
                next = self.planets_degree_ut[planets_degut[keys[1]]]
            elif e == (len(keys) - 1):
                prev = self.planets_degree_ut[planets_degut[keys[e - 1]]]
                next = self.planets_degree_ut[planets_degut[keys[0]]]
            else:
                prev = self.planets_degree_ut[planets_degut[keys[e - 1]]]
                next = self.planets_degree_ut[planets_degut[keys[e + 1]]]
            diffa = self.degreeDiff(prev, self.planets_degree_ut[i])
            diffb = self.degreeDiff(next, self.planets_degree_ut[i])
            planets_by_pos[e] = [i, diffa, diffb]
            # print "%s %s %s" % (self.planets[i]['label'],diffa,diffb)
            if (diffb < planet_drange):
                if group_open:
                    groups[-1].append([e, diffa, diffb, self.planets[planets_degut[keys[e]]]["label"]])
                else:
                    group_open = True
                    groups.append([])
                    groups[-1].append([e, diffa, diffb, self.planets[planets_degut[keys[e]]]["label"]])
            else:
                if group_open:
                    groups[-1].append([e, diffa, diffb, self.planets[planets_degut[keys[e]]]["label"]])
                group_open = False

        def zero(x):
            return 0

        planets_delta = list(map(zero, range(len(self.planets))))

        # print groups
        # print planets_by_pos
        for a in range(len(groups)):
            # Two grouped planets
            if len(groups[a]) == 2:
                next_to_a = groups[a][0][0] - 1
                if groups[a][1][0] == (len(planets_by_pos) - 1):
                    next_to_b = 0
                else:
                    next_to_b = groups[a][1][0] + 1
                # if both planets have room
                if (groups[a][0][1] > (2 * planet_drange)) & (groups[a][1][2] > (2 * planet_drange)):
                    planets_delta[groups[a][0][0]] = -(planet_drange - groups[a][0][2]) / 2
                    planets_delta[groups[a][1][0]] = +(planet_drange - groups[a][0][2]) / 2
                # if planet a has room
                elif (groups[a][0][1] > (2 * planet_drange)):
                    planets_delta[groups[a][0][0]] = -planet_drange
                # if planet b has room
                elif (groups[a][1][2] > (2 * planet_drange)):
                    planets_delta[groups[a][1][0]] = +planet_drange

                # if planets next to a and b have room move them
                elif (planets_by_pos[next_to_a][1] > (2.4 * planet_drange)) & (
                        planets_by_pos[next_to_b][2] > (2.4 * planet_drange)):
                    planets_delta[(next_to_a)] = (groups[a][0][1] - planet_drange * 2)
                    planets_delta[groups[a][0][0]] = -planet_drange * .5
                    planets_delta[next_to_b] = -(groups[a][1][2] - planet_drange * 2)
                    planets_delta[groups[a][1][0]] = +planet_drange * .5

                # if planet next to a has room move them
                elif (planets_by_pos[next_to_a][1] > (2 * planet_drange)):
                    planets_delta[(next_to_a)] = (groups[a][0][1] - planet_drange * 2.5)
                    planets_delta[groups[a][0][0]] = -planet_drange * 1.2

                # if planet next to b has room move them
                elif (planets_by_pos[next_to_b][2] > (2 * planet_drange)):
                    planets_delta[next_to_b] = -(groups[a][1][2] - planet_drange * 2.5)
                    planets_delta[groups[a][1][0]] = +planet_drange * 1.2

            # Three grouped planets or more
            xl = len(groups[a])
            if xl >= 3:

                available = groups[a][0][1]
                for f in range(xl):
                    available += groups[a][f][2]
                need = (3 * planet_drange) + (1.2 * (xl - 1) * planet_drange)
                leftover = available - need
                xa = groups[a][0][1]
                xb = groups[a][(xl - 1)][2]

                # center
                if (xa > (need * .5)) & (xb > (need * .5)):
                    startA = xa - (need * .5)
                # position relative to next planets
                else:
                    startA = (leftover / (xa + xb)) * xa
                    startB = (leftover / (xa + xb)) * xb

                if available > need:
                    planets_delta[groups[a][0][0]] = startA - groups[a][0][1] + (1.5 * planet_drange)
                    for f in range(xl - 1):
                        planets_delta[groups[a][(f + 1)][0]] = 1.2 * planet_drange + planets_delta[groups[a][f][0]] - \
                                                               groups[a][f][2]

        planets = dict()
        for e in range(len(keys)):
            i = planets_degut[keys[e]]

            # coordinates
            if self.type == "Transit":
                if 22 < i < 27:
                    rplanet = 76
                elif switch == 1:
                    rplanet = 110
                    switch = 0
                else:
                    rplanet = 130
                    switch = 1
            else:
                # if 22 < i < 27 it is asc,mc,dsc,ic (angles of chart)
                # put on special line (rplanet is range from outer ring)
                amin, bmin, cmin = 0, 0, 0
                if self.astrocfg["chartview"] == "european":
                    amin = 74 - 10
                    bmin = 94 - 10
                    cmin = 40 - 10

                if 22 < i < 27:
                    rplanet = 40 - cmin
                elif switch == 1:
                    rplanet = 74 - amin
                    switch = 0
                else:
                    rplanet = 94 - bmin
                    switch = 1

            rtext = 45
            # if self.astrocfg['houses_system'] == "G":
            #     offset = (int(self.houses_degree_ut[18]) / -1) + int(self.planets_degree_ut[i])
            # else:
            #     offset = (int(self.houses_degree_ut[6]) / -1) + int(self.planets_degree_ut[i]+planets_delta[e])
            #     trueoffset = (int(self.houses_degree_ut[6]) / -1) + int(self.planets_degree_ut[i])

            if self.astrocfg['houses_system'] == "G":
                offset = (self.houses_degree_ut[18] / -1) + self.planets_degree_ut[i]
            else:
                offset = (self.houses_degree_ut[6] / -1) + self.planets_degree_ut[i] + planets_delta[e]
                trueoffset = (int(self.houses_degree_ut[6]) / -1) + int(self.planets_degree_ut[i])

            new_offset = (self.houses_degree_ut[6] / -1) + self.planets_degree_ut[i]
            planets[self.planets[i]['name'].lower()] = {'angle': (new_offset + 360) % 360}

            planet_x = self.sliceToX(0, (r - rplanet), offset) + rplanet
            planet_y = self.sliceToY(0, (r - rplanet), offset) + rplanet

            # print("TRUE OFFSET {} : {}".format(self.planets[i]['name'], trueoffset))
            # print("     OFFSET {} : {}".format(self.planets[i]['name'], offset))
            # print(" NEW OFFSET {} : {}".format(
            #     self.planets[i]['name'],
            #     (self.houses_degree_ut[6] / -1) + self.planets_degree_ut[i],
            # ),
            # )
            angle = new_offset
            # angle = self.planets_degree_ut[i]
            degrees = int(angle)
            decimal = angle - degrees
            minutes = int(
                decimal * 60,
            )
            reliquat = decimal * 60 - minutes
            seconds = int(
                round(
                    reliquat * 60,
                )
            )
            print(
                "angle : {}°{:02} {:02}".format(
                    degrees,
                    minutes,
                    seconds,
                ),
            )

            if self.type == "Transit":
                scale = 0.8
            elif self.astrocfg["chartview"] == "european":
                scale = 0.8
                # line1
                x1 = self.sliceToX(0, (r - self.c3), trueoffset) + self.c3
                y1 = self.sliceToY(0, (r - self.c3), trueoffset) + self.c3
                x2 = self.sliceToX(0, (r - rplanet - 30), trueoffset) + rplanet + 30
                y2 = self.sliceToY(0, (r - rplanet - 30), trueoffset) + rplanet + 30
                color = self.planets[i]["color"]
                output += '<line x1="%s" y1="%s" x2="%s" y2="%s" style="stroke-width:1px;stroke:%s;stroke-opacity:.3;"/>\n' % (
                x1, y1, x2, y2, color)
                # line2
                x1 = self.sliceToX(0, (r - rplanet - 30), trueoffset) + rplanet + 30
                y1 = self.sliceToY(0, (r - rplanet - 30), trueoffset) + rplanet + 30
                x2 = self.sliceToX(0, (r - rplanet - 10), offset) + rplanet + 10
                y2 = self.sliceToY(0, (r - rplanet - 10), offset) + rplanet + 10
                output += '<line x1="%s" y1="%s" x2="%s" y2="%s" style="stroke-width:1px;stroke:%s;stroke-opacity:.5;"/>\n' % (
                x1, y1, x2, y2, color)
            else:
                scale = 1
            # output planet

            output = output + '<g transform="translate(-' + str(12 * scale) + ',-' + str(
                12 * scale) + ')"><g transform="scale(' + str(scale) + ')"><use x="' + str(
                planet_x * (1 / scale)) + '" y="' + str(planet_y * (1 / scale)) + '" xlink:href="#' + self.planets[i][
                         'name'] + '" /></g></g>\n'

        # make transit degut and display planets
        t_planets = dict()
        if self.type == "Transit":
            group_offset = {}
            t_planets_degut = {}
            for i in range(len(self.planets)):
                group_offset[i] = 0
                if self.planets[i]['visible'] == 1:
                    t_planets_degut[self.t_planets_degree_ut[i]] = i
            t_keys = list(t_planets_degut.keys())
            t_keys.sort()

            # grab closely grouped planets
            groups = []
            in_group = False
            for e in range(len(t_keys)):
                i_a = t_planets_degut[t_keys[e]]
                if e == (len(t_keys) - 1):
                    i_b = t_planets_degut[t_keys[0]]
                else:
                    i_b = t_planets_degut[t_keys[e + 1]]

                a = self.t_planets_degree_ut[i_a]
                b = self.t_planets_degree_ut[i_b]
                diff = self.degreeDiff(a, b)
                if diff <= 2.5:
                    if in_group:
                        groups[-1].append(i_b)
                    else:
                        groups.append([i_a])
                        groups[-1].append(i_b)
                        in_group = True
                else:
                    in_group = False
            # loop groups and set degrees display adjustment
            for i in range(len(groups)):
                if len(groups[i]) == 2:
                    group_offset[groups[i][0]] = -1.0
                    group_offset[groups[i][1]] = 1.0
                elif len(groups[i]) == 3:
                    group_offset[groups[i][0]] = -1.5
                    group_offset[groups[i][1]] = 0
                    group_offset[groups[i][2]] = 1.5
                elif len(groups[i]) == 4:
                    group_offset[groups[i][0]] = -2.0
                    group_offset[groups[i][1]] = -1.0
                    group_offset[groups[i][2]] = 1.0
                    group_offset[groups[i][3]] = 2.0

            switch = 0
            for e in range(len(t_keys)):
                i = t_planets_degut[t_keys[e]]

                if 22 < i < 27:
                    rplanet = 9
                elif switch == 1:
                    rplanet = 18
                    switch = 0
                else:
                    rplanet = 26
                    switch = 1

                zeropoint = 360 - self.houses_degree_ut[6]
                t_offset = zeropoint + self.t_planets_degree_ut[i]
                if t_offset > 360:
                    t_offset = t_offset - 360

                t_planets[self.planets[i]['name'].lower()] = {'angle': (t_offset + 360) % 360}

                planet_x = self.sliceToX(0, (r - rplanet), t_offset) + rplanet
                planet_y = self.sliceToY(0, (r - rplanet), t_offset) + rplanet
                output = output + '<g transform="translate(-6,-6)"><g transform="scale(0.5)"><use x="' + str(
                    planet_x * 2) + '" y="' + str(planet_y * 2) + '" xlink:href="#' + self.planets[i][
                             'name'] + '" /></g></g>\n'
                # transit planet line
                x1 = self.sliceToX(0, r + 3, t_offset) - 3
                y1 = self.sliceToY(0, r + 3, t_offset) - 3
                x2 = self.sliceToX(0, r - 3, t_offset) + 3
                y2 = self.sliceToY(0, r - 3, t_offset) + 3
                output = output + '<line x1="' + str(x1) + '" y1="' + str(y1) + '" x2="' + str(x2) + '" y2="' + str(
                    y2) + '" style="stroke: ' + self.planets[i][
                             'color'] + '; stroke-width: 1px; stroke-opacity:.8;"/>\n'

                # transit planet degree text
                rotate = self.houses_degree_ut[0] - self.t_planets_degree_ut[i]
                textanchor = "end"
                t_offset += group_offset[i]
                rtext = -3.0

                if -90 > rotate > -270:
                    rotate = rotate + 180.0
                    textanchor = "start"
                if 270 > rotate > 90:
                    rotate = rotate - 180.0
                    textanchor = "start"

                if textanchor == "end":
                    xo = 1
                else:
                    xo = -1
                deg_x = self.sliceToX(0, (r - rtext), t_offset + xo) + rtext
                deg_y = self.sliceToY(0, (r - rtext), t_offset + xo) + rtext
                degree = int(t_offset)
                output += '<g transform="translate(%s,%s)">' % (deg_x, deg_y)
                output += '<text transform="rotate(%s)" text-anchor="%s' % (rotate, textanchor)
                output += '" style="fill: ' + self.planets[i]['color'] + '; font-size: 10px;">' + self.dec2deg(
                    self.t_planets_degree[i], type="1")
                output += '</text></g>\n'

            # check transit
            if self.type == "Transit":
                dropin = 36
            else:
                dropin = 0

            # planet line
            x1 = self.sliceToX(0, r - (dropin + 3), offset) + (dropin + 3)
            y1 = self.sliceToY(0, r - (dropin + 3), offset) + (dropin + 3)
            x2 = self.sliceToX(0, (r - (dropin - 3)), offset) + (dropin - 3)
            y2 = self.sliceToY(0, (r - (dropin - 3)), offset) + (dropin - 3)
            output = output + '<line x1="' + str(x1) + '" y1="' + str(y1) + '" x2="' + str(x2) + '" y2="' + str(
                y2) + '" style="stroke: ' + self.planets[i]['color'] + '; stroke-width: 2px; stroke-opacity:.6;"/>\n'

            # check transit
            if self.type == "Transit":
                dropin = 160
            else:
                dropin = 120

            x1 = self.sliceToX(0, r - dropin, offset) + dropin
            y1 = self.sliceToY(0, r - dropin, offset) + dropin
            x2 = self.sliceToX(0, (r - (dropin - 3)), offset) + (dropin - 3)
            y2 = self.sliceToY(0, (r - (dropin - 3)), offset) + (dropin - 3)
            output = output + '<line x1="' + str(x1) + '" y1="' + str(y1) + '" x2="' + str(x2) + '" y2="' + str(
                y2) + '" style="stroke: ' + self.planets[i]['color'] + '; stroke-width: 2px; stroke-opacity:.6;"/>\n'

        return planets, t_planets

    def makePatterns(self):
        """
        * Stellium: At least four planets linked together in a series of continuous conjunctions.
        * Grand trine: Three trine aspects together.
        * Grand cross: Two pairs of opposing planets squared to each other.
        * T-Square: Two planets in opposition squared to a third.
        * Yod: Two qunicunxes together joined by a sextile.
        """
        conj = {}  # 0
        opp = {}  # 10
        sq = {}  # 5
        tr = {}  # 6
        qc = {}  # 9
        sext = {}  # 3
        for i in range(len(self.planets)):
            a = self.planets_degree_ut[i]
            qc[i] = {}
            sext[i] = {}
            opp[i] = {}
            sq[i] = {}
            tr[i] = {}
            conj[i] = {}
            # skip some points
            n = self.planets[i]['name']
            if n == 'earth' or n == 'true node' or n == 'osc. apogee' or n == 'intp. apogee' or n == 'intp. perigee':
                continue
            if n == 'Dsc' or n == 'Ic':
                continue
            for j in range(len(self.planets)):
                # skip some points
                n = self.planets[j]['name']
                if n == 'earth' or n == 'true node' or n == 'osc. apogee' or n == 'intp. apogee' or n == 'intp. perigee':
                    continue
                if n == 'Dsc' or n == 'Ic':
                    continue
                b = self.planets_degree_ut[j]
                delta = float(self.degreeDiff(a, b))
                # check for opposition
                xa = float(self.aspects[10]['degree']) - float(self.aspects[10]['orb'])
                xb = float(self.aspects[10]['degree']) + float(self.aspects[10]['orb'])
                if (xa <= delta <= xb):
                    opp[i][j] = True
                # check for conjunction
                xa = float(self.aspects[0]['degree']) - float(self.aspects[0]['orb'])
                xb = float(self.aspects[0]['degree']) + float(self.aspects[0]['orb'])
                if (xa <= delta <= xb):
                    conj[i][j] = True
                # check for squares
                xa = float(self.aspects[5]['degree']) - float(self.aspects[5]['orb'])
                xb = float(self.aspects[5]['degree']) + float(self.aspects[5]['orb'])
                if (xa <= delta <= xb):
                    sq[i][j] = True
                # check for qunicunxes
                xa = float(self.aspects[9]['degree']) - float(self.aspects[9]['orb'])
                xb = float(self.aspects[9]['degree']) + float(self.aspects[9]['orb'])
                if (xa <= delta <= xb):
                    qc[i][j] = True
                # check for sextiles
                xa = float(self.aspects[3]['degree']) - float(self.aspects[3]['orb'])
                xb = float(self.aspects[3]['degree']) + float(self.aspects[3]['orb'])
                if (xa <= delta <= xb):
                    sext[i][j] = True

        yot = {}
        # check for double qunicunxes
        for k, v in qc.items():
            if len(qc[k]) >= 2:
                # check for sextile
                for l, w in qc[k].items():
                    for m, x in qc[k].items():
                        if m in sext[l]:
                            if l > m:
                                yot['%s,%s,%s' % (k, m, l)] = [k, m, l]
                            else:
                                yot['%s,%s,%s' % (k, l, m)] = [k, l, m]
        tsquare = {}
        # check for opposition
        for k, v in opp.items():
            if len(opp[k]) >= 1:
                # check for square
                for l, w in opp[k].items():
                    for a, b in sq.items():
                        if k in sq[a] and l in sq[a]:
                            # print 'got tsquare %s %s %s' % (a,k,l)
                            if k > l:
                                tsquare['%s,%s,%s' % (a, l, k)] = '%s => %s, %s' % (
                                    self.planets[a]['label'], self.planets[l]['label'], self.planets[k]['label'])
                            else:
                                tsquare['%s,%s,%s' % (a, k, l)] = '%s => %s, %s' % (
                                    self.planets[a]['label'], self.planets[k]['label'], self.planets[l]['label'])
        stellium = {}
        # check for 4 continuous conjunctions
        for k, v in conj.items():
            if len(conj[k]) >= 1:
                # first conjunction
                for l, m in conj[k].items():
                    if len(conj[l]) >= 1:
                        for n, o in conj[l].items():
                            # skip 1st conj
                            if n == k:
                                continue
                            if len(conj[n]) >= 1:
                                # third conjunction
                                for p, q in conj[n].items():
                                    # skip first and second conj
                                    if p == k or p == n:
                                        continue
                                    if len(conj[p]) >= 1:
                                        # fourth conjunction
                                        for r, s in conj[p].items():
                                            # skip conj 1,2,3
                                            if r == k or r == n or r == p:
                                                continue

                                            l = [k, n, p, r]
                                            l.sort()
                                            stellium['%s %s %s %s' % (l[0], l[1], l[2], l[3])] = '%s %s %s %s' % (
                                                self.planets[l[0]]['label'], self.planets[l[1]]['label'],
                                                self.planets[l[2]]['label'], self.planets[l[3]]['label'])
        # print yots
        out = '<g transform="translate(-30,380)">'
        if len(yot) >= 1:
            y = 0
            for k, v in yot.items():
                out += '<text y="%s" style="fill:%s; font-size: 12px;">%s</text>\n' % (y, self.colors['paper_0'], "Yot")

                # first planet symbol
                out += '<g transform="translate(20,%s)">' % (y)
                out += '<use transform="scale(0.4)" x="0" y="-20" xlink:href="#%s" /></g>\n' % (
                    self.planets[yot[k][0]]['name'])

                # second planet symbol
                out += '<g transform="translate(30,%s)">' % (y)
                out += '<use transform="scale(0.4)" x="0" y="-20" xlink:href="#%s" /></g>\n' % (
                    self.planets[yot[k][1]]['name'])

                # third planet symbol
                out += '<g transform="translate(40,%s)">' % (y)
                out += '<use transform="scale(0.4)" x="0" y="-20" xlink:href="#%s" /></g>\n' % (
                    self.planets[yot[k][2]]['name'])

                y = y + 14
        # finalize
        out += '</g>'
        # return out
        return ''

    def makeAspects(self, r=240, ar=0):
        aspects = []
        out = ""
        for i in range(len(self.planets)):
            start = self.planets_degree_ut[i]
            for x in range(i):
                end = self.planets_degree_ut[x]
                diff = float(self.degreeDiff(start, end))
                # loop orbs
                if (self.planets[i]['visible_aspect_line'] == 1) & (self.planets[x]['visible_aspect_line'] == 1):
                    for z in range(len(self.aspects)):
                        if (float(self.aspects[z]['degree']) - float(self.aspects[z]['orb'])) <= diff <= (
                                float(self.aspects[z]['degree']) + float(self.aspects[z]['orb'])):
                            # check if we want to display this aspect
                            if self.aspects[z]['visible'] == 1:
                                offset1 = (int(self.houses_degree_ut[6]) / -1) + int(self.planets_degree_ut[i])
                                offset2 = (int(self.houses_degree_ut[6]) / -1) + int(self.planets_degree_ut[x])
                                aspect = {
                                    'angles': [offset1, offset2],
                                    'aspect': self.aspects[z],
                                    'planets': [
                                        self.planets[i],
                                        self.planets[x],
                                    ]
                                }
                                aspects.append(aspect)
                                # out = out + self.drawAspect( r , ar , self.planets_degree_ut[i] , self.planets_degree_ut[x] , self.colors["aspect_%s" %(self.aspects[z]['degree'])] )
        return aspects

    def makeAspectsTransit(self):
        aspects = []
        out = ""
        self.atgrid = []
        for i in range(len(self.planets)):
            start = self.planets_degree_ut[i]
            for x in range(i + 1):
                end = self.t_planets_degree_ut[x]
                diff = float(self.degreeDiff(start, end))
                # loop orbs
                if (self.planets[i]['visible'] == 1) & (self.planets[x]['visible'] == 1):
                    for z in range(len(self.aspects)):
                        # check for personal planets and determine orb
                        if 0 <= i <= 4 or 0 <= x <= 4:
                            orb_before = 1.0
                        else:
                            orb_before = 2.0
                        # check if we want to display this aspect
                        if (float(self.aspects[z]['degree']) - orb_before) <= diff <= (
                                float(self.aspects[z]['degree']) + 1.0):
                            if self.aspects[z]['visible'] == 1:
                                # out = out + self.drawAspect(r, ar, self.planets_degree_ut[i],
                                #                             self.t_planets_degree_ut[x],
                                #                             self.colors["aspect_%s" % (self.aspects[z]['degree'])])
                                offset1 = (int(self.houses_degree_ut[6]) / -1) + int(self.planets_degree_ut[i])
                                offset1 = (offset1 + 360) % 360
                                offset2 = 360 - self.houses_degree_ut[6] + int(self.t_planets_degree_ut[x])
                                offset2 = (offset2 + 360) % 360
                                aspect = {
                                    'angles': [offset1, offset2],
                                    'aspect': self.aspects[z],
                                    'planets': [
                                        self.planets[i],
                                        self.planets[x],
                                    ]
                                }
                                aspects.append(aspect)
                            # aspect grid dictionary
                            # if self.aspects[z]['visible_grid'] == 1:
                            #     self.atgrid.append({})
                            #     self.atgrid[-1]['p1'] = i
                            #     self.atgrid[-1]['p2'] = x
                            #     self.atgrid[-1]['aid'] = z
                            #     self.atgrid[-1]['diff'] = diff
        return aspects

    def makeAspectTransitGrid(self, r):
        out = '<g transform="translate(500,310)">'
        out += '<text y="-15" x="0" style="fill:%s; font-size: 12px;">%s</text>\n' % (
        self.colors['paper_0'], "Planets in Transit")
        line = 0
        nl = 0
        for i in range(len(self.atgrid)):
            if i == 12:
                nl = 100
                if len(self.atgrid) > 24:
                    line = -1 * (len(self.atgrid) - 24) * 14
                else:
                    line = 0
            out += '<g transform="translate(%s,%s)">' % (nl, line)
            # first planet symbol
            out += '<use transform="scale(0.4)" x="0" y="3" xlink:href="#%s" />\n' % (
                self.planets[self.atgrid[i]['p2']]['name'])
            # aspect symbol
            out += '<use  x="15" y="0" xlink:href="#orb%s" />\n' % (
                self.aspects[self.atgrid[i]['aid']]['degree'])
            # second planet symbol
            out += '<g transform="translate(30,0)">'
            out += '<use transform="scale(0.4)" x="0" y="3" xlink:href="#%s" />\n' % (
                self.planets[self.atgrid[i]['p1']]['name'])
            out += '</g>'
            # difference in degrees
            out += '<text y="8" x="45" style="fill:%s; font-size: 10px;">%s</text>' % (
                self.colors['paper_0'],
                self.dec2deg(self.atgrid[i]['diff']))
            # line
            out += '</g>'
            line = line + 14
        out += '</g>'
        return out

    def makeAspectGrid(self, r):
        out = ""
        style = 'stroke:%s; stroke-width: 1px; stroke-opacity:.6; fill:none' % (self.colors['paper_0'])
        xindent = 380
        yindent = 468
        box = 14
        revr = list(range(len(self.planets)))
        revr.reverse()
        for a in revr:
            if self.planets[a]['visible_aspect_grid'] == 1:
                start = self.planets_degree_ut[a]
                # first planet
                out = out + '<rect x="' + str(xindent) + '" y="' + str(yindent) + '" width="' + str(
                    box) + '" height="' + str(box) + '" style="' + style + '"/>\n'
                out = out + '<use transform="scale(0.4)" x="' + str((xindent + 2) * 2.5) + '" y="' + str(
                    (yindent + 1) * 2.5) + '" xlink:href="#' + self.planets[a]['name'] + '" />\n'
                xindent = xindent + box
                yindent = yindent - box
                revr2 = list(range(a))
                revr2.reverse()
                xorb = xindent
                yorb = yindent + box
                for b in revr2:
                    if self.planets[b]['visible_aspect_grid'] == 1:
                        end = self.planets_degree_ut[b]
                        diff = self.degreeDiff(start, end)
                        out = out + '<rect x="' + str(xorb) + '" y="' + str(yorb) + '" width="' + str(
                            box) + '" height="' + str(box) + '" style="' + style + '"/>\n'
                        xorb = xorb + box
                        for z in range(len(self.aspects)):
                            if (float(self.aspects[z]['degree']) - float(self.aspects[z]['orb'])) <= diff <= (
                                    float(self.aspects[z]['degree']) + float(self.aspects[z]['orb'])) and \
                                    self.aspects[z]['visible_grid'] == 1:
                                out = out + '<use  x="' + str(xorb - box + 1) + '" y="' + str(
                                    yorb + 1) + '" xlink:href="#orb' + str(self.aspects[z]['degree']) + '" />\n'
        return out

    def makeElements(self, r):
        total = self.fire + self.earth + self.air + self.water
        pf = int(round(100 * self.fire / total))
        pe = int(round(100 * self.earth / total))
        pa = int(round(100 * self.air / total))
        pw = int(round(100 * self.water / total))
        out = '<g transform="translate(-30,79)">\n'
        out = out + '<text y="0" style="fill:#ff6600; font-size: 10px;">' + self.label['fire'] + '  ' + str(
            pf) + '%</text>\n'
        out = out + '<text y="12" style="fill:#6a2d04; font-size: 10px;">' + self.label['earth'] + ' ' + str(
            pe) + '%</text>\n'
        out = out + '<text y="24" style="fill:#6f76d1; font-size: 10px;">' + self.label['air'] + '   ' + str(
            pa) + '%</text>\n'
        out = out + '<text y="36" style="fill:#630e73; font-size: 10px;">' + self.label['water'] + ' ' + str(
            pw) + '%</text>\n'
        out = out + '</g>\n'
        return out

    def makePlanetGrid(self):
        out = '<g transform="translate(510,-40)">'
        # loop over all planets
        li = 10
        offset = 0
        for i in range(len(self.planets)):
            if i == 27:
                li = 10
                offset = -120
            if self.planets[i]['visible'] == 1:
                # start of line
                out = out + '<g transform="translate(%s,%s)">' % (offset, li)
                # planet text
                out = out + '<text text-anchor="end" style="fill:%s; font-size: 10px;">%s</text>' % (
                self.colors['paper_0'], self.planets[i]['label'])
                # planet symbol
                out = out + '<g transform="translate(5,-8)"><use transform="scale(0.4)" xlink:href="#' + \
                      self.planets[i]['name'] + '" /></g>'
                # planet degree
                out = out + '<text text-anchor="start" x="19" style="fill:%s; font-size: 10px;">%s</text>' % (
                self.colors['paper_0'], self.dec2deg(self.planets_degree[i]))
                # zodiac
                out = out + '<g transform="translate(60,-8)"><use transform="scale(0.3)" xlink:href="#' + self.zodiac[
                    self.planets_sign[i]] + '" /></g>'
                # planet retrograde
                if self.planets_retrograde[i]:
                    out = out + '<g transform="translate(74,-6)"><use transform="scale(.5)" xlink:href="#retrograde" /></g>'

                # end of line
                out = out + '</g>\n'
                # offset between lines
                li = li + 14

        out = out + '</g>\n'
        return out

    def makeHousesGrid(self):
        out = '<g transform="translate(610,-40)">'
        li = 10
        for i in range(12):
            if i < 9:
                cusp = '&#160;&#160;' + str(i + 1)
            else:
                cusp = str(i + 1)
            out += '<g transform="translate(0,' + str(li) + ')">'
            out += '<text text-anchor="end" x="40" style="fill:%s; font-size: 10px;">%s %s:</text>' % (
            self.colors['paper_0'], self.label['cusp'], cusp)
            out += '<g transform="translate(40,-8)"><use transform="scale(0.3)" xlink:href="#' + self.zodiac[
                self.houses_sign[i]] + '" /></g>'
            out += '<text x="53" style="fill:%s; font-size: 10px;"> %s</text>' % (
            self.colors['paper_0'], self.dec2deg(self.houses_degree[i]))
            out += '</g>\n'
            li = li + 14
        out += '</g>\n'
        return out

    """Export/Import Functions related to openastro.org

    def exportOAC(filename)
    def importOAC(filename)
    def importOroboros(filename)

    """

    def exportOAC(self, filename):
        template = """<?xml version='1.0' encoding='UTF-8'?>
<openastrochart>
    <name>$name</name>
    <datetime>$datetime</datetime>
    <location>$location</location>
    <altitude>$altitude</altitude>
    <latitude>$latitude</latitude>
    <longitude>$longitude</longitude>
    <countrycode>$countrycode</countrycode>
    <timezone>$timezone</timezone>
    <geonameid>$geonameid</geonameid>
    <timezonestr>$timezonestr</timezonestr>
    <extra>$extra</extra>
</openastrochart>"""
        h, m, s = self.decHour(openAstro.hour)
        dt = datetime.datetime(openAstro.year, openAstro.month, openAstro.day, h, m, s)
        substitute = {}
        substitute['name'] = self.name
        substitute['datetime'] = dt.strftime("%Y-%m-%d %H:%M:%S")
        substitute['location'] = self.location
        substitute['altitude'] = self.altitude
        substitute['latitude'] = self.geolat
        substitute['longitude'] = self.geolon
        substitute['countrycode'] = self.countrycode
        substitute['timezone'] = self.timezone
        substitute['timezonestr'] = self.timezonestr
        substitute['geonameid'] = self.geonameid
        substitute['extra'] = ''
        # write the results to the template
        output = Template(template).substitute(substitute)
        f = open(filename, "w")
        f.write(output)
        f.close()
        dprint("exporting OAC: %s" % filename)
        return

    def importOAC(self, filename):
        r = importfile.getOAC(filename)[0]
        dt = datetime.datetime.strptime(r['datetime'], "%Y-%m-%d %H:%M:%S")
        self.name = r['name']
        self.countrycode = r['countrycode']
        self.altitude = int(r['altitude'])
        self.geolat = float(r['latitude'])
        self.geolon = float(r['longitude'])
        self.timezone = float(r['timezone'])
        self.geonameid = r['geonameid']
        if "timezonestr" in r:
            self.timezonestr = r['timezonestr']
        else:
            self.timezonestr = self.db.gnearest(self.geolat, self.geolon)['timezonestr']
        self.location = r['location']
        self.year = dt.year
        self.month = dt.month
        self.day = dt.day
        self.hour = self.decHourJoin(dt.hour, dt.minute, dt.second)
        # Make locals
        self.utcToLocal()
        # debug print
        dprint('importOAC: %s' % filename)
        return

    def importOroboros(self, filename):
        r = importfile.getOroboros(filename)[0]
        # naive local datetime
        naive = datetime.datetime.strptime(r['datetime'], "%Y-%m-%d %H:%M:%S")
        # aware datetime object
        dt_input = datetime.datetime(naive.year, naive.month, naive.day, naive.hour, naive.minute, naive.second)
        dt = pytz.timezone(r['zoneinfo']).localize(dt_input)
        # naive utc datetime object
        dt_utc = dt.replace(tzinfo=None) - dt.utcoffset()

        # process latitude/longitude
        deg, type, min, sec = r['latitude'].split(":")
        lat = float(deg) + (float(min) / 60.0) + (float(sec) / 3600.0)
        if type == "S":
            lat = decimal / -1.0
        deg, type, min, sec = r['longitude'].split(":")
        lon = float(deg) + (float(min) / 60.0) + (float(sec) / 3600.0)
        if type == "W":
            lon = decimal / -1.0

        geon = self.db.gnearest(float(lat), float(lon))
        self.timezonestr = geon['timezonestr']
        self.geonameid = geon['geonameid']
        self.name = r['name']
        self.countrycode = ''
        self.altitude = int(r['altitude'])
        self.geolat = lat
        self.geolon = lon
        self.timezone = self.offsetToTz(dt.utcoffset())
        self.location = '%s, %s' % (r['location'], r['countryname'])
        self.year = dt_utc.year
        self.month = dt_utc.month
        self.day = dt_utc.day
        self.hour = self.decHourJoin(dt_utc.hour, dt_utc.minute, dt_utc.second)
        # Make locals
        self.utcToLocal()
        # debug print
        dprint('importOroboros: UTC: %s file: %s' % (dt_utc, filename))
        return

    def importSkylendar(self, filename):
        r = importfile.getSkylendar(filename)[0]

        # naive local datetime
        naive = datetime.datetime(int(r['year']), int(r['month']), int(r['day']), int(r['hour']), int(r['minute']))
        # aware datetime object
        dt_input = datetime.datetime(naive.year, naive.month, naive.day, naive.hour, naive.minute, naive.second)
        dt = pytz.timezone(r['zoneinfofile']).localize(dt_input)
        # naive utc datetime object
        dt_utc = dt.replace(tzinfo=None) - dt.utcoffset()

        geon = self.db.gnearest(float(r['latitude']), float(r['longitude']))
        self.timezonestr = geon['timezonestr']
        self.geonameid = geon['geonameid']
        self.name = r['name']
        self.countrycode = ''
        self.altitude = 25
        self.geolat = float(r['latitude'])
        self.geolon = float(r['longitude'])
        self.timezone = float(r['timezone'])
        self.location = '%s, %s' % (r['location'], r['countryname'])
        self.year = dt_utc.year
        self.month = dt_utc.month
        self.day = dt_utc.day
        self.hour = self.decHourJoin(dt_utc.hour, dt_utc.minute, dt_utc.second)
        # Make locals
        self.utcToLocal()
        return

    def importAstrolog32(self, filename):
        r = importfile.getAstrolog32(filename)[0]

        # timezone string
        timezone_str = zonetab.nearest_tz(float(r['latitude']), float(r['longitude']), zonetab.timezones())[2]
        # naive local datetime
        naive = datetime.datetime(int(r['year']), int(r['month']), int(r['day']), int(r['hour']), int(r['minute']),
                                  int(r['second']))
        # aware datetime object
        dt_input = datetime.datetime(naive.year, naive.month, naive.day, naive.hour, naive.minute, naive.second)
        dt = pytz.timezone(timezone_str).localize(dt_input)
        # naive utc datetime object
        dt_utc = dt.replace(tzinfo=None) - dt.utcoffset()

        geon = self.db.gnearest(float(r['latitude']), float(r['longitude']))
        self.timezonestr = geon['timezonestr']
        self.geonameid = geon['geonameid']
        self.name = r['name']
        self.countrycode = ''
        self.altitude = 25
        self.geolat = float(r['latitude'])
        self.geolon = float(r['longitude'])
        self.timezone = self.offsetToTz(dt.utcoffset())
        self.location = r['location']
        self.year = dt_utc.year
        self.month = dt_utc.month
        self.day = dt_utc.day
        self.hour = self.decHourJoin(dt_utc.hour, dt_utc.minute, dt_utc.second)
        # Make locals
        self.utcToLocal()
        return

    def importZet8(self, filename):
        h = open(filename)
        f = codecs.EncodedFile(h, "utf-8", "latin-1")
        data = []
        for line in f.readlines():
            s = line.split(";")
            if s[0] == line:
                continue

            data.append({})
            data[-1]['name'] = s[0].strip()
            day = int(s[1].strip().split('.')[0])
            month = int(s[1].strip().split('.')[1])
            year = int(s[1].strip().split('.')[2])
            hour = int(s[2].strip().split(':')[0])
            minute = int(s[2].strip().split(':')[1])
            if len(s[3].strip()) > 3:
                data[-1]['timezone'] = float(s[3].strip().split(":")[0])
                if data[-1]['timezone'] < 0:
                    data[-1]['timezone'] -= float(s[3].strip().split(":")[1]) / 60.0
                else:
                    data[-1]['timezone'] += float(s[3].strip().split(":")[1]) / 60.0
            elif len(s[3].strip()) > 0:
                data[-1]['timezone'] = int(s[3].strip())
            else:
                data[-1]['timezone'] = 0

            # substract timezone from date
            dt = datetime.datetime(year, month, day, hour, minute)
            dt = dt - datetime.timedelta(seconds=float(data[-1]['timezone']) * float(3600))
            data[-1]['year'] = dt.year
            data[-1]['month'] = dt.month
            data[-1]['day'] = dt.day
            data[-1]['hour'] = float(dt.hour) + float(dt.minute / 60.0)
            data[-1]['location'] = s[4].strip()

            # latitude
            p = s[5].strip()
            if p.find("°") != -1:
                # later version of zet8
                if p.find("S") == -1:
                    deg = p.split("°")[0]  # \xc2
                    min = p[p.find("°") + 2:p.find("'")]
                    sec = p[p.find("'") + 1:p.find('"')]
                    data[-1]['latitude'] = float(deg) + (float(min) / 60.0)
                else:
                    deg = p.split("°")[0]  # \xc2
                    min = p[p.find("°") + 2:p.find("'")]
                    sec = p[p.find("'") + 1:p.find('"')]
                    data[-1]['latitude'] = (float(deg) + (float(min) / 60.0)) / -1.0
            else:
                # earlier version of zet8
                if p.find("s") == -1:
                    i = p.find("n")
                    data[-1]['latitude'] = float(p[:i]) + (float(p[i + 1:]) / 60.0)
                else:
                    i = p.find("s")
                    data[-1]['latitude'] = (float(p[:i]) + (float(p[i + 1:]) / 60.0)) / -1.0
            # longitude
            p = s[6].strip()
            if p.find("°") != -1:
                # later version of zet8
                if p.find("W") == -1:
                    deg = p.split("°")[0]  # \xc2
                    min = p[p.find("°") + 2:p.find("'")]
                    sec = p[p.find("'") + 1:p.find('"')]
                    data[-1]['longitude'] = float(deg) + (float(min) / 60.0)
                else:
                    deg = p.split("°")[0]  # \xc2
                    min = p[p.find("°") + 2:p.find("'")]
                    sec = p[p.find("'") + 1:p.find('"')]
                    data[-1]['longitude'] = (float(deg) + (float(min) / 60.0)) / -1.0
            else:
                # earlier version of zet8
                if p.find("w") == -1:
                    i = p.find("e")
                    data[-1]['longitude'] = float(p[:i]) + (float(p[i + 1:]) / 60.0)
                else:
                    i = p.find("w")
                    data[-1]['longitude'] = (float(p[:i]) + (float(p[i + 1:]) / 60.0)) / -1.0

        self.db.importZet8(cfg.peopledb, data)
        dprint('importZet8: database with %s entries: %s' % (len(data), filename))
        f.close()
        return


# debug print function
def dprint(str):
    if "--debug" in sys.argv or DEBUG:
        print('%s' % str)
