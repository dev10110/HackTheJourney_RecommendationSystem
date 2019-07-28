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

        self.headers = {
            'Authorization': 'Bearer ' + j['access_token']
        }

    def get_poi(self, lat, lon, rad=20, lim=1000, name=''):

        poi_endpoint = 'reference-data/locations/pois'
        poi_url = self.base_url + poi_endpoint
        poi_params = {
            'latitude': lat,
            'longitude': lon,
            'page[limit]': lim,
            'r': rad
        }

        r = requests.get(poi_url, headers=self.headers, params=poi_params)

        data = json.loads(r.text)['data']

        # add in the city name
        for el in data:
            el['city'] = name

        return data

    def build_default_data(self, kpercity=20):
        # builds the data set for the default list of cities
        cities = pd.read_csv('defaultCities.csv')
        data = []

        for i in range(len(cities)):
            try:
                citydata = self.get_poi(lat=cities['Latitude'][i], lon=cities['Longitude'][i],
                                        name=cities['Name'][i].lower(), lim=kpercity)
                print('Loaded city: %s, with %i POIs' % (cities['Name'][i], len(citydata)))
                data += citydata
            except:
                print('Failed city: %s' % cities['Name'][i])

        return data

    def get_iata_city(self, city_name: str) -> str:
        """

        :param city_name: city name to get IATA code for

        :return: returns IATA code
        """

        endpoint = "reference-data/locations"
        url = self.base_url + endpoint

        params = {
            "subType": "CITY",
            "keyword": city_name
        }

        data = requests.get(url, params=params, headers=self.headers).json().get("data")

        if data:
            return data[0].get("iataCode")

        else: return ""

    def get_city_iata(self, iata_code: str) -> str:
        """

        :param iata_code: iata code to get city for

        :return: returns city name
        """

        endpoint = "reference-data/locations"
        url = self.base_url + endpoint

        params = {
            "subType": "CITY",
            "keyword": iata_code
        }

        data = requests.get(url, params=params, headers=self.headers).json().get("data")

        if data:
            return data[0].get("address").get("cityName")

        else:
            return ""


    def get_inspiration(self, origin: str,
                        startdate: datetime.date = None,
                        enddate: datetime.date = None,
                        maxPrice: int = None,
                        currency: str = "GBP") -> List[dict]:

        """

        :param origin: 3 Letter IATA city code of origin city
        :param startdate: start Date for date timerange, defaults to now()
        :param enddate: end Date for date timerange, can be left out
        :param maxPrice: maxPrice for the flight, defaults to 65536
        :param currency: currency of the maxPrice parameter, defaults to GBP

        :return:
        """
        inspiration_endpoint = 'shopping/flight-destinations'
        inspiration_url = self.base_url + inspiration_endpoint

        params = {
            'origin': origin,
            'departureDate': f"{startdate.strftime('%Y-%m-%d') if startdate else datetime.datetime.now().strftime('%Y-%m-%d')}"
            f"{(',' + enddate.strftime('%Y-%m-%d')) if enddate else ''}",
            "currency": currency,
            "maxPrice": maxPrice if maxPrice else 65536
        }

        res = requests.get(inspiration_url, headers=self.headers, params=params)

        if res.status_code == 500:

            # TODO: low fare search
            raise Exception(f"No data found for city code {origin}")

        return res.json().get("data")