import pickle

from AmadeusClient import AmadeusClient

am = AmadeusClient()

#data = am.get_poi(lat=51.50, lon=-0.177)
data = am.get_poi(lat=41.39715, lon=2.160873)

#pickle.dump(data, open('london_poi.pickle', 'wb'))
pickle.dump(data, open('spain_poi.pickle', 'wb'))
