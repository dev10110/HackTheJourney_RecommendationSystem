import datetime
from typing import List

from flask import Flask, jsonify, request, abort
from recommender.RecommenderClient import RecommenderClient
from data_import.AmadeusClient import AmadeusClient
from planner.PlannerClient import GoogleMapsClient
import pickle
import settings
import sys
import json
import logging


app = Flask(__name__)
logger = logging.getLogger(__name__)
settings.load_dotenv()


client = RecommenderClient()
ac = AmadeusClient()
google = GoogleMapsClient()


data = pickle.load(open("final_data.pkl", "rb"))
client.add_data(data.get("data"), create_model=True)
client.cities_added.union(data.get("cities"))


def checkCitysAndAdd(city_iatas: List[str]) -> List[str]:
    """Checks if cities contained in recommender data and add data

    :param city_iatas: iata codes for cities to add to recommender

    :return:
    """

    city_names = []
    for city in city_iatas:
        if not city in client.cities_added:
            logger.debug(f"City {city} not in data, performing lookup and adding to data")

            city_name = ac.get_city_iata(city)
            city_names.append(city_name)

            lat_long = google.getLatLongCity(city_name)

            tmp_data = ac.get_poi(lon=lat_long.get("lng"), lat=lat_long.get("lat"), name=city)

            data['data'] += tmp_data
            data['cities'] += city

            client.add_data(tmp_data, city=city, create_model=False)

        else:
            logger.debug(f"City {city} is already contained in recommenderModel")

    logger.debug("Storing new data in pkl file")
    pickle.dump(data, open("final_data.pkl", "wb"))

    logger.debug("Creating model with new data")
    client.create_model()

    return city_names

@app.route("/")
def index():
    return "Take a look a the Readme.md :]"


@app.route("/getPOI")
def getPOI() -> List[dict]:
    """
    :keyword limit: set limit for returned POI's, defaults to 10

    :return: List of POI's
    """

    limit = request.args.get("limit", 10)

    return jsonify(client.cold_start(k=limit))


@app.route("/getRecommendations")
def getRecommendations():
    likes = request.args.get("likes")
    limit = request.args.get("limit", 10)

    if not likes:
        abort(400, "Missing parameter likes")

    try:
        likes = json.loads(likes)

    except json.JSONDecodeError as e:
        print(e)
        abort(400, "Invalid data in likes parameter")

    result = client.suggest(k=limit, likes=likes)

    return jsonify(client.recs2data(result, df=False))


@app.route("/getIATA")
def getIATA():
    """Returns IATA code for given city

    :keyword: city: city to return IATA code for
    """

    return ac.get_iata_city(request.args.get("city"))


@app.route("/getCITY")
def getCITY():
    """Returns city name for given IATA code

    :keyword: iata: iata code to get city for
    """

    return ac.get_city_iata(request.args.get("iata"))


@app.route("/generateInspiration")
def generateInspiration():
    """
    :keyword: likes: List of likes corresponing with indecies of POI's
    :keyword: origin: IATA Code from where flight should originate from, defaults to LON
    :keyword: budget: limit recommended flights to flights inside budget
    :keyword: limit_activities: limit amount of recommended activities per city, defaults to 10
    :keyword: limit_inspirations: limit amount of inspirations, defaults to 10

    :return: -
    """

    likes = request.args.get("likes")
    origin = request.args.get("origin", "LON")
    budget = request.args.get("budget")
    limit_inspirations = int(request.args.get("limit_inspirations", 10))
    limit_activities = int(request.args.get("limit_activities", 10))
    startdate = request.args.get("startdate")

    if not likes:
        abort(400, "Missing parameter likes")

    try:
        likes = json.loads(likes)

    except json.JSONDecodeError as e:
        print(e)
        abort(400, "Invalid data in likes parameter")

    if startdate:
        startdate = datetime.datetime.strptime(startdate, "%Y-%m-%d")

    cities = ac.get_inspiration(origin, maxPrice=budget, limit=limit_inspirations,
                                startdate=startdate)

    city_iata_codes = [city.get("destination") for city in cities]
    city_names = checkCitysAndAdd(city_iata_codes)

    for index, city in enumerate(cities):
        cities[index]["city-name"] = city_names[index]
        recommendations = client.suggest(likes=likes, cities=city.get("destination"), k=limit_activities)
        recommendations_dict = client.recs2data(recommendations, df=False)
        cities[index]["activities"] = recommendations_dict
        cities[index]["itinerary"] = google.generate_itinerary(recommendations_dict)

    return jsonify(cities)


if __name__ == "__main__":
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    app.run("0.0.0.0", 8080, debug=False, threaded=True)
