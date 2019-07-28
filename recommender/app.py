from typing import List

from flask import Flask, jsonify, request, abort
from RecommenderClient import RecommenderClient
from data_import.AmadeusClient import AmadeusClient
import pickle
import json

app = Flask(__name__)


client = RecommenderClient()
ac = AmadeusClient()

# TODO: convert data into (data, cities)
# TODO: convert cities names into IATA Codes
data = pickle.load(open("../data_import/all_data.pkl", "rb"))
client.add_data(data, create_model=True)


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

    limit = request.args.get("limit", 10)

    # todo: startdate and enddate parameters
    if not likes:
        abort(400, "Missing parameter likes")

    try:
        likes = json.loads(likes)

    except json.JSONDecodeError as e:
        print(e)
        abort(400, "Invalid data in likes parameter")

    cities = ac.get_inspiration(origin, budget=budget)

    # todo: check if city is in recommender data
    # if not: # todo: call poi for city
              # todo: add data to recommender data
    # todo: return list of cities with top x recommended activities


if __name__ == "__main__":
    app.run("localhost", 8080, debug=True, threaded=True)
