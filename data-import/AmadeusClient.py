import requests

import json
import os
import pandas as pd

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

	build_default_data(self, kpercity = 20):
		#builds the data set for the default list of cities
		cities = pd.read_csv('defaultCities.csv')

		data = []
		for i in range(len(cities)):
		    citydata = self.get_poi(lat=cities['Latitude'][i], lon=cities['Longitude'][i], name=cities['Name'][i],lim=kpercity)
		    print('Loaded city: %s'%cities['Name'][i])
		    data += citydata

		return data
