from flask import Flask, jsonify, request, abort
from RecommenderClient import RecommenderClient
import pickle
import json
import random

app = Flask(__name__)


client = RecommenderClient()
data = pickle.load(open("../data-import/all_data.pkl", "rb"))
client.add_data(data, create_model=True)


@app.route("/index")
def index():
    return "Call /getRecommendations"


@app.route("/getPOI")
def getPOI():

    limit = request.args.get("limit", 10)

    choices = random.choices(data, k=limit)

    return jsonify(choices)


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


if __name__ == "__main__":
    app.run("localhost", 8080, debug=True, threaded=True)
