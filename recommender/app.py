from typing import List

from flask import Flask, jsonify, request, abort
from RecommenderClient import RecommenderClient
from data_import.AmadeusClient import AmadeusClient
import pickle
import json
import logging


app = Flask(__name__)
logger = logging.getLogger(__name__)


client = RecommenderClient()
ac = AmadeusClient()


data = pickle.load(open("final_data.pkl", "rb"))
client.add_data(data.get("data"), create_model=True)
client.cities_added += set(data.get("cities"))


def checkCitysAndAdd(city_iatas: List[str]):
    """Checks if cities contained in recommender data and add data

    :param city_iatas: iata codes for cities to add to recommender

    :return:
    """

    for city in city_iatas:
        if not city in client.cities_added:
            logger.debug(f"City {city} not in data, performing lookup and adding to data")

            # todo: convert city name to long, lat
            tmp_data = ac.get_poi(lon=1, lat=1, city=city)

            data['data'] += tmp_data
            data['cities'] += city

            client.add_data(tmp_data, city=city, create_model=False)

        else:
            logger.debug(f"City {city} is already contained in recommenderModel")

    logger.debug("Storing new data in pkl file")
    pickle.dump(data, open("final_data.pkl", "wb"))

    logger.debug("Creating model with new data")
    client.create_model()


@app.route("/index")
def index():
    return "Call /getRecommendations"


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


@app.route("/generateInspiration")
def generateInspiration():
    """
    :keyword: likes: List of likes corresponing with indecies of POI's
    :keyword: origin: IATA Code from where flight should originate from, defaults to LON
    :keyword: budget: limit recommended flights to flights inside budget
    :keyword: limit: limit amount of recommended activities per city

    :return: -
    """

    likes = request.args.get("likes")
    origin = request.args.get("origin", "LON")
    budget = request.args.get("budget")
    limit_inspirations = request.args.get("limit_inspirations", 10)
    limit_activities = request.args.get("limit_activities", 10)

    # todo: startdate and enddate parameters

    if not likes:
        abort(400, "Missing parameter likes")

    try:
        likes = json.loads(likes)

    except json.JSONDecodeError as e:
        print(e)
        abort(400, "Invalid data in likes parameter")

    cities = ac.get_inspiration(origin, budget=budget, limit=limit_inspirations)

    city_iata_codes = [city.get("destination") for city in cities]
    checkCitysAndAdd(city_iata_codes)

    output = []
    for city in city_iata_codes:

        recommendations = client.suggest(likes, cities=city, k=limit_activities)
        recommendations_dict = client.recs2data(recommendations, df=False)

        output.append({
            "city": city,
            "activies": recommendations_dict
        })


if __name__ == "__main__":
    app.run("localhost", 8080, debug=True, threaded=True)
