import requests

import json
import datetime
import os
import pandas as pd
from typing import List


class AmadeusClient:
	base_url = 'https://api.amadeus.com/v1/'
	auth_token = ''

	def __init__(self):
		self.get_token()


	def get_token(self):
		auth_endpoint = 'security/oauth2/token'
		auth_url = self.base_url + auth_endpoint
		auth_data = {
			'grant_type': 'client_credentials',
			'client_id': os.environ.get('CLIENT_ID'),
			'client_secret': os.environ.get('CLIENT_SECRET')
		}
		auth_headers = {
			'content-type': 'application/x-www-form-urlencoded'
		}
		r = requests.post(auth_url, data=auth_data, headers=auth_headers)
		j = json.loads(r.text)
		self.auth_token = j['access_token']



	def get_poi(self, lat, lon, rad=20, lim=1000, name=''):

		poi_endpoint = 'reference-data/locations/pois'
		poi_url = self.base_url + poi_endpoint
		poi_params = {
			'latitude': lat,
			'longitude': lon,
			'page[limit]': lim,
			'r': rad
		}
		poi_headers = {
			'Authorization': 'Bearer ' + self.auth_token
		}

		r = requests.get(poi_url, headers=poi_headers, params=poi_params)

		data = json.loads(r.text)['data']

		# add in the city name
		for el in data:
			el['city'] = name


		return data

	def build_default_data(self, kpercity = 20):
		#builds the data set for the default list of cities
		cities = pd.read_csv('defaultCities.csv')
		data = []

		for i in range(len(cities)):
		    try:
		        citydata = self.get_poi(lat=cities['Latitude'][i], lon=cities['Longitude'][i], name=cities['Name'][i].lower(),lim=kpercity)
		        print('Loaded city: %s, with %i POIs' % (cities['Name'][i], len(citydata)))
		        data += citydata
		    except:
		        print('Failed city: %s' % cities['Name'][i])

		return data

	def get_inspiration(self, origin: str,
						startdate: datetime.date = None,
						enddate: datetime.date = None,
						maxPrice: int = None,
						currency: str = "GBP") -> List[dict]:

		inspiration_endpoint = 'shopping/flight-destinations'
		inspiration_url = self.base_url + inspiration_endpoint

		params = {
			'origin': origin,
			'departureDate': f"{startdate.strftime('%Y-%m-%d') if startdate else datetime.datetime.now()}"
					         f"{(',' + enddate.strftime('%Y-%m-%d')) if enddate else ''}",
			"currency": currency,
			"maxPrice": maxPrice if maxPrice else 65536
		}
		headers = {
			'Authorization': 'Bearer ' + self.auth_token
		}

		r = requests.get(inspiration_url, headers=headers, params=params)
		return json.loads(r.text)['data']
