#!/usr/bin/env python3
"""TODO."""

from sys import argv

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, StaticFileHandler

import simplejson as json
import configparser

DEFAULT_CONFIG = {'global': {'name': 'Sonne', 'port': 8080}}

sonne = None # global access to application object

class Sonne:
    def __init__(self):
        self.config = None
        self.cities = []
        self.application = Application([
            (r'/', IndexHandler),
            (r'/api/query', QueryEndpoint),
            (r'/static/lib/(.*)', StaticFileHandler, {'path': 'node_modules'}),
            (r'/static/(.*)', StaticFileHandler, {'path': 'static'})
        ], debug=True)

    def run(self):
        self.loadConfig()
        self.loadData()

        port = self.config['global']['port']
        self.application.listen(port)
        print('Listening on port {}'.format(port))
        IOLoop.current().start()

    def loadConfig(self):
        config = configparser.ConfigParser()
        config.read_dict(DEFAULT_CONFIG)
        try:
            config.read('site.cfg')
        except:
            print('Could not read site.cfg!')
        self.config = config

    def loadData(self):
        data = json.load(open('wwis.json'))
        for item in data.values():
            name = item['cityName']
            country = item['country']
            #if not 'climateMonth' in item['climate']:
            climate_month = item['climate']['climateMonth']
            if len(climate_month) != 12: # or not climate_month[0]['maxTemp']:
                print('Warning: No climate data for {}, skipping'.format(name))
                continue
            maxtemps = [float(m['maxTemp'] or 'nan') for m in climate_month]
            mintemps = [float(m['minTemp'] or 'nan') for m in climate_month]
            try:
                raindays = [int(float(m['raindays'] or -1)) for m in climate_month]
            except ValueError as e:
                print('Warning: Corrupt rainday data ({}), skipping'.format(e))
            latlong = (float(item['cityLatitude']), float(item['cityLongitude']))
            self.cities.append(City(name, country, maxtemps, mintemps, raindays, latlong))
        print('Read climate data for {} cities'.format(len(self.cities)))

class City:
    def __init__(self, name, country, maxtemps, mintemps, raindays, latlong):
        self.name = name
        self.country = country
        self.maxtemps = maxtemps
        self.mintemps = mintemps
        self.raindays = raindays
        self.latlong = latlong

class IndexHandler(RequestHandler):
    def get(self):
        data = {
            'title': sonne.config['global']['name']
        }
        self.render('index.html', **data)

class QueryEndpoint(RequestHandler):
    def get(self):
        temp = int(self.get_query_argument('temp'))
        if not (-50 <= temp <= 50):
            raise ValueError('temp')
        month = int(self.get_query_argument('month'))
        if not (0 <= month <= 11):
            raise ValueError('month')
        latlong = self.get_query_argument('latlong', None)
        if latlong:
            latlong = latlong.split(',')
            latlong = float(latlong[0]), float(latlong[1])
        print('latlong', latlong)

        # Naive query
        cities = [dict(vars(c)) for c in sonne.cities if temp - 2 <= c.maxtemps[month] <= temp + 2]

        if latlong:
            for city in cities:
                city['dist'] = distance(latlong, city['latlong'])
            cities.sort(key=lambda c: c['dist'])

        self.write(json.dumps(cities, ignore_nan=True))

def distance(frm, to):
	return haversine(frm[0], frm[1], to[0], to[1])
# XXX: stackoverflow copy
from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

if __name__ == '__main__':
    sonne = Sonne()
    sonne.run()
