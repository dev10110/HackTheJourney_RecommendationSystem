import pickle
import pandas
import os

os.chdir('../data-import/')
from AmadeusClient import AmadeusClient

am = AmadeusClient()


#build default data
recData = am.build_default_data()

#create the cold guess
rc = RecommenderClient()
rc.add_data(recData,create_model=False)
rc.create_model()
cold_guess = rc.cold_start(k=30)


print(rc.ind2data(cold_guess))

#pick likes
likes = [7, 88, 56]

#choose city
berlinlat, berlinlon = 52.5067614,13.2846511

#get berlin data
berlin_data = am.get_poi(lat = berlinlat, lon = berlinlon, name='Berlin')
rc.add_data(berlin_data,city = 'berlin', create_model=True)

#get recommendations
recs = rc.suggest(k = 10, likes = likes,categories= ['SIGHTS', 'SHOPPING', 'NIGHTLIFE'],  cities='Berlin')

print(recs)

rc.recs2data(recs, df=True)
