import pymongo as pymongo
from bson import json_util
from flask import Flask, request, jsonify, json
from flask import Response
import json
import requests
import requests.exceptions
from pymongo import MongoClient
from bson.objectid import ObjectId

api_url = "http://172.20.10.2:5000/contacts/"


def get_api_url():
    return api_url


app = Flask(__name__)

try:
    client = MongoClient("mongodb://my_mongo_db:27017")
    g_database_name = "storeDB"
    g_collection_name = "game_collection"
    #client.drop_database('storeDB')
    db = client.storeDB
    games = db["games"]
    client.server_info()
except Exception as ex:
    print(ex)
    print("Unable to connect to database XD")

db.games.insert_one({"title": "Mario","releaseYear": 1994, "genre": "platformer", "price": 10, "length": 60, "buyer_id":"12345"})
db.games.insert_one({"title": "CIV5","releaseYear": 2015, "genre": "strategy", "price": 55, "length": "not specified", "buyer_id":""})
db.games.insert_one({"title": "Stellaris","releaseYear": 2016, "genre": "strategy", "price": 99, "length": "not specified", "buyer_id":""})



@app.route("/api/v2/games", methods=['POST'])
def add_game():
    try:
        game = {"title": request.form["title"],
                "releaseYear": request.form["releaseYear"],
                "genre": request.form["genre"],
                "price": request.form["price"],
                "length": request.form["length"],
                "buyer_id": ""
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
        if dbResponse["buyer_id"] is not None:
            api_url = get_api_url()
            api_url = api_url + str(dbResponse["buyer_id"])
            try:
                response = requests.get(api_url)
                response.raise_for_status()
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                         print("bad")
                         return Response(
                             response=json.dumps(dbResponse, default=str),
                             status=200,
                             mimetype="application/json"
                         )
            except requests.exceptions.HTTPError:
                         print("bad2")
                         return Response(
                             response=json.dumps(dbResponse, default=str),
                             status=200,
                             mimetype="application/json"
                         )
            else:
                            if  response.status_code == 200:
                                converterJs = json.loads(response.text)
                                response2 = {
                                    "_id": dbResponse['_id'],
                                    "title": dbResponse['title'],
                                    "releaseYear": dbResponse['releaseYear'],
                                    "genre": dbResponse['genre'],
                                    "price": dbResponse['price'],
                                    "length": dbResponse['length'],
                                    "buyer": [
                                        {
                                            "id": converterJs['id'],
                                            "surname": converterJs['surname'],
                                            "name": converterJs['name'],
                                            "number": converterJs['number'],
                                            "email": converterJs['email']
                                        }
                                    ]
                                }
                                return Response(
                                    response=json.dumps(response2, default=str),
                                    status=200,
                                    mimetype="application/json"
                                )
                            else:
                                print(response.status_code)
                                return Response(
                                    response=json.dumps(dbResponse, default=str),
                                    status=200,
                                    mimetype="application/json"
                                )
        else:
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
                                            "length": request.form["length"],
                                            "buyer": request.form["buyer"]}})
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

@app.route("/api/v2/games/<id>/buyer", methods=["GET"])
def get_game_buyer(id):
    game = db.games.find_one({'_id': ObjectId(id)})
    try:
        if game is None:
            return Response(
                json.dumps({"Error": "No such id for a game exists"}),
                status=404,
                mimetype="application/json",
            )
        buyer_id = game.get("buyer_id")
        print(buyer_id)
        if buyer_id:
            api_url = get_api_url()
            api_url = api_url + str(buyer_id)
            response = requests.get(api_url)

            return Response(
                response.text,
                status=response.status_code,
                mimetype="application/json",
            )
        else:
            return Response(
                json.dumps({"Error": "This game has no buyer"}),
                status=404,
                mimetype="application/json",
            )
    except Exception as ex:
        print(ex)
        return Response(
            json.dumps({"Error": "Cannot get game buyer " + str(ex)}),
            status= 500,
            mimetypes="application/json")


@app.route("/api/v2/games/<id>/buyer", methods=["POST"])
def add_game_buyer(id):
    game = db.games.find_one({'_id': ObjectId(id)})
    buyer_id = request.form["buyer_id"]
    print(buyer_id)
    print("--------------------------------------------------------------------------")
    print("game: ", game)
    try:
        if game is None:
            return Response(
                json.dumps({"Error": "No game with this id exists"}),
                status=404,
                mimetype="application/json",
            )
        #print(buyer_id)
        if game["buyer_id"] != "":
            return Response(
                json.dumps({"Error": "Game already has a buyer!"}),
                status=404,
                mimetype="application/json",
            )
        else:
            api_url = get_api_url()
            api_url = api_url + str(buyer_id)
            response = requests.get(api_url)
            print(response.status_code)
            if response.status_code == 200:
                    db.games.update_one({"_id": ObjectId(id)},{"$set": {"buyer_id": buyer_id}})
                    return Response(
                            json.dumps({"Success": "Game buyer added successfully"}),
                            status=200,
                            mimetype="application/json",
                            headers={"Location": '/games/{}'.format(id) + "/buyer"}
                            )
            else:
                return Response(
                            json.dumps({"Error" : "Could not find a buyer with this id"}),
                            status=404,
                            mimetype="application/json"
                            )
    except Exception as ex:
        print(ex)
        return Response(
            json.dumps({"Error": "Encountered an error: " + str(ex)}),
            status = 500,
            mimetypes="application/json")


@app.route("/api/v2/games/<id>/buyer", methods=["DELETE"])
def del_game_buyer(id):
    game = db.games.find_one({'_id': ObjectId(id)})
    try:
        if game is None:
            return Response(
                json.dumps({"Error": "No game with this id exists"}),
                status=404,
                mimetype="application/json",
            )
        #print(buyer_id)
        if game["buyer_id"] != "":
            db.games.update_one({"_id": ObjectId(id)}, {"$set": {"buyer_id": ""}})
            return Response(
                json.dumps({"Success": "Game buyer deleted successfully"}),
                status=200,
                mimetype="application/json",
                headers={"Location": '/games/{}'.format(id) + "/buyer"}
            )
        else:
            print(":: No buyer to delete")
            return Response(
                            json.dumps({"Error": "Game doesnt have a buyer to delete!"}),
                            status=404,
                            mimetype="application/json"
                            )
    except Exception as ex:
        print(ex)
        return Response(
            json.dumps({"Error": "Encountered an error: " + str(ex)}),
            status= 500,
            mimetypes="application/json")


@app.route("/api/v2/games/<id>/buyer", methods=["PATCH"])
def update_game_buyer(id):
    game = db.games.find_one({'_id': ObjectId(id)})
    buyer_id = request.form["buyer_id"]
    try:
        if game is None:
            return Response(
                json.dumps({"Error": "No game with this id exists"}),
                status=404,
                mimetype="application/json",
            )
        #print(buyer_id)
        if game["buyer_id"] != "":
            api_url = get_api_url()
            api_url = api_url + str(buyer_id)
            response = requests.get(api_url)
            if response.status_code == 200:
                db.games.update_one({"_id": ObjectId(id)}, {"$set": {"buyer_id": buyer_id}})
                return Response(
                    json.dumps({"Success": "Game buyer updated successfully"}),
                    status=200,
                    mimetype="application/json",
                    headers={"Location": '/games/{}'.format(id) + "/buyer"}
                )
            else:
                return Response(
                    json.dumps({"Error": "Could not find a buyer with this id"}),
                    status=404,
                    mimetype="application/json",
                )
        else:
                return Response(
                    json.dumps({"Error": "Nothing to update!"}),
                    status=404,
                    mimetype="application/json",
                )
    except Exception as ex:
        print(ex)
        return Response(
            json.dumps({"Error": "Encountered an error: " + str(ex)}),
            status = 500,
            mimetypes="application/json")


@app.route("/api/v2/games/buyer", methods=["POST"])
def add_contact():
    try:
        contact = {"id": request.form["id"],
                "surname": request.form["surname"],
                "name": request.form["name"],
                "number": request.form["number"],
                "email": request.form["email"],
                }
        print(contact)
        jsonify(contact)
        print(contact)
        response2 = requests.post(api_url, json = contact)
        response2.text
        return Response(
                response2.text,
                  status=200,
                  mimetype="application/json",
               )


    except Exception as ex:
        print(ex)

        return Response(
            response=json.dumps({"message": "Adding the contact failed",
                                 "error": str(ex)}),
            status=500,
            mimetype="application/json"
        )


@app.route("/api/v2/games/buyer", methods=["GET"])
def get_contacts():
    try:
              response = requests.get(api_url)
              response = response.text
              return Response(
                    response,
                    status=200,
                    mimetype="application/json",
                )

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Server is down",
                                 "error": str(ex)}),
            status=404,
            mimetype="application/json"
        )


if __name__=='__main__':
    app.run(host="0.0.0.0", debug = True, port=80)