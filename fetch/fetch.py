#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Greedy climate data fetch
"""

filename = 'wwis.json'
indexurl = 'http://worldweather.wmo.int/en/json/full_city_list.txt'
baseurl = 'http://worldweather.wmo.int/en/json/{0}_en.xml'
guideurl = 'http://worldweather.wmo.int/en/dataguide.html'
notice = 'Please note the guidelines at {0}'
usage = """{0} <index file> [output file]

Data will be downloaded into {1} if no second argument given.
The full index file is available for download at {2}
You can re-run this script to continue downloading in the case of failures."""

from sys import argv
import urllib.request
import csv
import simplejson as json
import time
import sys

def fetch_entry(id):
	url = baseurl.format(id)
	try:
		f = urllib.request.urlopen(url).read()
		entry = json.loads(f.decode())
	except:
		return -1
	time.sleep(0.1) # don't DoS
	return entry

def nice_entry(entry, country):
	data = entry['city']
	data['country'] = country
	return data

if __name__ == '__main__':
	if len(argv) < 2:
		print(usage.format(argv[0], filename, indexurl))
		exit(1)

	print(notice.format(guideurl))

	if len(argv) > 2:
		filename = argv[2]

	data = {}
	try:
		with open(filename, 'r') as f:
			data = json.load(f)
	except:
		pass

	with open(argv[1], 'r', newline='') as f:
		reader = csv.reader(f, delimiter=';', quotechar='"')
		for row in reader:
			if len(row) < 3:
				print('?', end='', file=sys.stderr)
				continue
			if row[0] == 'Country':
				continue
			key = row[2]
			if key in data:
				print('✓', end='', file=sys.stderr)
				continue
			sys.stderr.flush()
			entry = fetch_entry(key)
			if entry == -1:
				print('⚡', end='', file=sys.stderr)
				break # bail out, save what we have
			print('.', end='', file=sys.stderr)
			data[key] = nice_entry(entry, row[0])
		print('', file=sys.stderr)

	with open(filename, 'w') as f:
		json.dump(data, f, sort_keys=True, indent='\t')
