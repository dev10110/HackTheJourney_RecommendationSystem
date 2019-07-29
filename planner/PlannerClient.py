import pandas as pd
import random
import googlemaps
from datetime import datetime

import tsp #solves the travelling salesman problem

class GoogleMapsClient():
    def __init__(self):

        self.gmaps = googlemaps.Client(key=os.environ['mapsAPI'])
        self.poi_latlon = None

    def get_place_ids_from_POIs(self,pois):
        #accept list of pois

        candidates = []

        for i in range(len(pois)):
            location_bias_string = f"point:{pois[i]['geoCode']['latitude']},{pois[i]['geoCode']['longitude']}"
            candidate = self.gmaps.find_place(input = pois[i]['name'], input_type='textquery',fields=['place_id'],location_bias=location_bias_string)

            candidates.append(candidate['candidates'][0]['place_id']) #extracts the first poi

        return candidates

    def get_mean_location(self,pois):
        #uses pois returned by amadeus
        poi_latlon = [pois[i]['geoCode'] for i in range(len(pois))]
        self.poi_latlon = pd.DataFrame.from_dict(poi_latlon).mean().to_dict()

        return  self.poi_latlon


    def generate_itinerary(self, pois, hotel_lat_lon = None):
        #assume hotel is dictionary of  in the style of {'latitude': 50.085133, 'longitude': 14.424776}
        #if not provided, the hotel is assumed to be at the mean location of the pois.
        #pois are list of pois generated by amadeus
        #result is a dictionary, that has:
        #    result['path'] is the path to be taken, indexed by pois
        #    result['travel_time'] is the matrix of travel times from a poi (row) to another poi (col). Note, indexes are shifted up by 1 due to hotel being added as index 0.
        #    result['dist_matrix'] is the distances matrix returned by google.

        if hotel_lat_lon is None:
            hotel_lat_lon = self.get_mean_location(pois)

        #convert pois to lat long
        poi_latlon = self.poi_latlon = [pois[i]['geoCode'] for i in range(len(pois))]
        #saved for future reference


        #collate
        full_latlon = [hotel_lat_lon] + poi_latlon
        num_of_points = len(full_latlon)

        #generate distance matrix from google
        dist_matrix = self.gmaps.distance_matrix(full_latlon,full_latlon,mode='transit')

        #generate summary of travel times (each number is the number of seconds of travel)
        travel_time = [[dist_matrix['rows'][o]['elements'][d]['duration']['value'] for d in range(num_of_points)] for o in range(num_of_points)]


        #convert to dictionary
        r = range(len(travel_time))
        cost = {(i,j): travel_time[i][j] for i in r for j in r}

        #solve travelling salesman problem
        (totaltime, path) = tsp.tsp(r, cost)

        #correct index, because hotel was added at point 0
        poi_path = [loc-1 for loc in path[1:]]

        result = dict()
        result['path'] = poi_path
        result['dist_matrix'] = dist_matrix
        result['travel_time'] = travel_time

        return result

    def get_details(self, place_name,location_bias=None):
        #assumes the place_name is a text to query
        if location_bias is not None:
            candidate = self.gmaps.find_place(input = place_name, input_type='textquery',fields=['place_id'], location_bias_string=location_bias)
        else:
            candidate = self.gmaps.find_place(input = place_name, input_type='textquery',fields=['place_id'])

        try:
            place_id = candidate['candidates'][0]['place_id'] #extracts the first poi
            details = self.gmaps.place(place_id)
            latlon = details['result']['geometry']['location']
            return {'place_id': place_id, 'latlon': latlon,'details':details}
        except:
            print('Error: Possibly, didnt find enough candidates?')




    def get_transit_directions(self,origin, destination, location_bias=None, mode='transit', summarise = True):
        #assume origin is either in a amadeus style or is a text entry for google maps search

        if location_bias is None:
            try:
                location_bias = self.poi_latlon

            except:
                pass

        if type(origin) is str:
            origin_details = self.get_details(origin, location_bias=location_bias)
            origin_latlon = origin_details['latlon']
        elif 'latitude' in origin.keys():
            origin_latlon = origin
        else:
            #assumes it is a amadeus location
            origin_latlon = origin['geoCode']

        if type(destination) is str:
            dest_details = self.get_details(destination, location_bias=location_bias)
            dest_latlon = dest_details['latlon']
        elif 'latitude' in destination.keys():
            destination_latlon = destination
        else:
            dest_latlon = destination['geoCode']

        transit = self.gmaps.directions(origin_latlon,dest_latlon,mode='transit')

        if summarise:
            return self.get_transit_summary(transit)
        else:
            return transit







    def get_transit_summary(self,transit):
        summary = dict()

        summary['total_time'] = transit[0]['legs'][0]['duration']['text']


        legs = dict()
        for i in range(len(transit_dir[0]['legs'][0]['steps'])):

            dur_string  = transit_dir[0]['legs'][0]['steps'][i]['duration']['text']
            description = transit_dir[0]['legs'][0]['steps'][i]['html_instructions']

            legs[i] = {'duration': dur_string, 'text': description}

        summary['legs'] = legs

        return summary
        