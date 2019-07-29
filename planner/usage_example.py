# example useage
import os
os.chdir('../data-import/')

from AmadeusClient import AmadeusClient

am = AmadeusClient()

os.chdir('../planner/')

#get list of pois
pois = am.get_poi(lat = 50.089848, lon = 14.432865)
pois = random.sample(pois, k = 9)



client = GoogleMapsClient()


#return the google maps place id from the pois
placeids = client.get_place_ids_from_POIs(pois)

# find the mean location from a set of amadeus style points of interest
hotel=client.get_mean_location(pois)

#create a itinerary
#note, there can only be 9 points of interest, excluding the hotel, since the distacne matrix can only take 10 locations.
itinerary = client.generate_itinerary(pois = pois, hotel_lat_lon= hotel)
#return the path of the itinerary
path = itinerary['path']
