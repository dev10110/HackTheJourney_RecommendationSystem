import requests
import json
import pickle
import os

base_url = 'https://api.amadeus.com/v1/'

auth_endpoint = 'security/oauth2/token'
auth_url = base_url + auth_endpoint
data = {
	'grant_type': 'client_credentials',
	'client_id': os.environ.get('CLIENT_ID'),
	'client_secret': os.environ.get('CLIENT_SECRET') 
}
headers = {
	'content-type': 'application/x-www-form-urlencoded'
}
r = requests.post(auth_url, data=data, headers=headers)
j = json.loads(r.text)
token = j['access_token']




poi_endpoint = 'reference-data/locations/pois'
poi_url = base_url + poi_endpoint
params = {
	'latitude': 51.50,
	'longitude': -0.177,
	'page[limit]': 1000,
	'r': 20
}
headers = {
	'Authorization': 'Bearer ' + token
}

r = requests.get(poi_url, headers=headers, params=params)
j = json.loads(r.text)['data']
pickle.dump(j, open('london_poi.pickle', 'wb'))
