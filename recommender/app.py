from flask import Flask, jsonify, request, abort
from RecommenderClient import RecommenderClient
import pickle
import json


app = Flask(__name__)
data = pickle.load(open("london_poi.pickle", "rb"))
client = RecommenderClient(data)


@app.route("/index")
def index():
    return "Call /getRecommendations"


@app.route("/getRecommendations")
def getRecommendations():

    likes = request.args.get("likes")

    if not likes:
        abort(400, "Missing parameter likes")

    try:
        likes = json.loads(likes)

    except json.JSONDecodeError as e:
        print(e)
        abort(400, "Invalid data in likes parameter")

    out = list()

    for entry in client.suggest(likes=likes):
        entry["data"] = data[entry.get("index")]
        out.append(entry)

    return jsonify(out)


if __name__ == "__main__":
    app.run("localhost", 8080, debug=True, threaded=True)
