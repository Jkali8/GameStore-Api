import pymongo as pymongo
from bson import json_util
from flask import Flask, request, jsonify, json
from flask import Response
import json
from jsonschema import validate
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)
try:
    client = pymongo.MongoClient(host = 'localhost',
                                  port =  27017,
                                  serverSelectionTimeoutMS = 1000)
    client.drop_database('storeDB')
    db = client.storeDB
    client.server_info()
except:
    print("Unable to connect to database")

db.games.insert_one({"title": "Mario","releaseYear": 1994, "genre": "platformer", "price": 10, "length": 60})
db.games.insert_one({"title": "CIV5","releaseYear": 2015, "genre": "strategy", "price": 55, "length": "not specified"})
db.games.insert_one({"title": "Stellaris","releaseYear": 2016, "genre": "strategy", "price": 99, "length": "not specified"})


def parse_json(data):
    return json.loads(json_util.dumps(data))


@app.route("/api/v2/games", methods=['POST'])
def add_game():
    try:
        game = {"title": request.form["title"],
                "releaseYear": request.form["releaseYear"],
                "genre": request.form["genre"],
                "price": request.form["price"],
                "length": request.form["length"]
                }
        dbResponse = db.games.insert_one(game)
        print(dbResponse.inserted_id)
        #for attr in dir(dbResponse):
         #   print(attr)
        return Response(
            response=json.dumps({"message": "Game added successfully",
                                 "gameId": str(dbResponse.inserted_id)}),
            status=200,
            mimetype="application/json",
            headers = {"Location": '/games/{}'.format(id)}
        )

    except Exception as ex:
        print(ex)

        return Response(
            response=json.dumps({"message": "Adding the game failed",
                                 "error": str(ex)}),
            status=500,
            mimetype="application/json"
        )


@app.route("/api/v2/games", methods=['GET'])
def get_games():
    try:
        data = list(db.games.find())
        print(data)
        for game in data:
            game["_id"] = str(game["_id"])
        return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Cannot retrieve games",
                                 "error": str(ex)}),
            status=500,
            mimetype="application/json"
        )


@app.route("/api/v2/games/<id>", methods=['GET'])
def get_game(id):
    try:
        dbResponse = db.games.find_one({'_id': ObjectId(id)})
        #print(data)
        return Response(
            response=json.dumps(dbResponse, default=str),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Cannot retrieve game",
                                 "error": str(ex)}),
            status=500,
            mimetype="application/json"
        )


@app.route("/api/v2/games/<id>", methods=['PUT'])
def update_game(id):
    try:
            dbResponse = db.games.update_one({"_id": ObjectId(id)},
                                             {"$set": {"title": request.form["title"],
                                            "releaseYear": request.form["releaseYear"],
                                            "genre": request.form["genre"],
                                            "price": request.form["price"],
                                            "length": request.form["length"]}})
            if dbResponse.modified_count == 0:
                return Response(
                    response=json.dumps({"message": "No updates made on : " + id}),
                    status=404,
                    mimetype="application/json"
                )
            else:
                return Response(
                    response=json.dumps({"message": "Game updated successfully",
                                         "gameId": id}),
                    status=200,
                    mimetype="application/json",
                    headers = {"Location": '/games/{}'.format(id)}
                )

    except Exception as ex:
            print(ex)
            return Response(
                     response=json.dumps({"message": "Cannot update game",
                             "error": str(ex)}),
                     status=500,
                     mimetype="application/json"
                        )


@app.route("/api/v2/games/<id>", methods=['PATCH'])
def updates_game(id):
    try:
        dbResponse = db.games.find_one({"_id": ObjectId(id)})
        if dbResponse is None:
            return Response(
                response=json.dumps({"message": "No game with id: " + id + " found"}),
                status=404,
                mimetype="application/json"
            )
        title = request.form["title"]
        releaseYear = request.form["releaseYear"]
        genre = request.form["genre"]
        price = request.form["price"]
        length = request.form["length"]
        if title == "" and releaseYear == "" and genre == "" and price == "" and length == "":
                return Response(
                    response=json.dumps({"message": "No values given to update on : " + id}),
                    status=404,
                    mimetype="application/json"
                )
        if title != "":
             db.games.update_one({"_id": ObjectId(id)},{"$set": {"title": title}})
        if releaseYear != "" and releaseYear > '1960':
             db.games.update_one({"_id": ObjectId(id)},{"$set": {"releaseYear": releaseYear}})
        if genre != "":
             db.games.update_one({"_id": ObjectId(id)},{"$set": {"genre": genre}})
        if price != "" and price == "0" and price > '0':
             db.games.update_one({"_id": ObjectId(id)},{"$set": {"price": price}})
        if length != "" and length == "0" and length > '0' or length == "not specified":
             db.games.update_one({"_id": ObjectId(id)},{"$set": {"length": length}})

        return Response(
                response=json.dumps({"message": "Game updated successfully",
                                     "gameId": id}),
                status=200,
                mimetype="application/json",
                headers = {"Location": '/games/{}'.format(id)}
            )

    except Exception as ex:
            print(ex)
            return Response(
                     response=json.dumps({"message": "Cannot update game",
                             "error": str(ex)}),
                     status=500,
                     mimetype="application/json"
                        )


@app.route("/api/v2/games/<id>", methods=['DELETE'])
def delete_game(id):
    try:
        dbResponse = db.games.delete_one({"_id": ObjectId(id)})
        if dbResponse.deleted_count == 0:
            return Response(
                response=json.dumps({"message": "No games with id: " + id}),
                status=404,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({"message": "Game deleted successfully",
                                     "gameId": id}),
                status=200,
                mimetype="application/json"
            )

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Cannot delete game" + str(ex)}),
                                status=500,
                                mimetype="application/json"
                 )


if __name__=='__main__':
    app.run(host="0.0.0.0", debug = True, port=80)