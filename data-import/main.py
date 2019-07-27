import pickle

from AmadeusClient import AmadeusClient

am = AmadeusClient()

data = am.get_poi(lat=51.50, lon=-0.177)

pickle.dump(data, open('london_poi.pickle', 'wb'))