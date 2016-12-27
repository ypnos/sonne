"""TODO."""

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, StaticFileHandler

import json

class Sonne:
    def __init__(self):
        self.cities = []
        self.application = Application([
            (r'/', IndexHandler),
            (r'/api/query', QueryEndpoint),
            (r'/static/lib/(.*)', StaticFileHandler, {'path': 'node_modules'})
        ], debug=True, app=self)

    def run(self):
        # TODO load cities data from db dump
        self.cities = [City('Berlin', 23), City('New York', 12)]

        self.application.listen(8080)
        IOLoop.current().start()

class City:
    def __init__(self, name, temp):
        self.name = name
        self.temp = temp

class IndexHandler(RequestHandler):
    def get(self):
        self.render('index.html')

class QueryEndpoint(RequestHandler):
    def get(self):
        temp = int(self.get_query_argument('temp'))
        if not (0 <= temp <= 100):
            raise ValueError('temp')
        month = int(self.get_query_argument('month'))
        if not (0 <= month <= 11):
            raise ValueError('month')

        # Naive query
        app = self.application.settings['app']
        cities = [c for c in app.cities if temp - 2 <= c.temp <= temp + 2]

        self.write(json.dumps([vars(c) for c in cities]))

if __name__ == '__main__':
    Sonne().run()
