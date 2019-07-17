from flask import request
from flask_restplus import Resource
from pymongo import errors
from bson.objectid import ObjectId
from voting_for_films import api, films, voting, history_of_voting, film_rating


@api.route('/films')
class Films(Resource):
    def get(self):
        output = []
        for q in films.find():
            output.append({"name": q["name"], "genre": q["genre"]})
        return {"result": output}, 200

    def post(self):
        name = request.form["name"]
        genre = request.form.getlist("genre")
        if name and genre:
            try:
                films.insert_one({"name": name, "genre": genre})
                output = {"name": name, "genre": genre}
                return {"result": output, "message": "Film created successfully!"}, 200
            except errors.DuplicateKeyError:
                return {"message": "Name already exists!"}, 400
        return {"message": "Bad request parameters!"}, 400


@api.route('/films/<string:name>')
class FilmsItem(Resource):
    def get(self, name):
        film = films.find_one({"name": name})
        if film:
            output = {"name": film["name"], "genre": film["genre"]}
            return {"result": output}, 200
        return {"message": "no record found"}, 404

    def post(self, name):
        new_genre = request.form.getlist("genre")
        if new_genre:
            try:
                films.insert_one({"name": name, "genre": new_genre})
                output = {"name": name, "genre": new_genre}
                return {"result": output, "message": "Film created successfully!"}, 200
            except errors.DuplicateKeyError:
                return {"message": "Name already exists!"}, 400
        return {"message": "Bad request parameters!"}, 400

    def put(self, name):
        new_name = request.form.getlist("name")
        new_genre = request.form.getlist("genre")
        if new_genre and new_name:
            result = films.find_one_and_update({"name": name}, {"$set": {"name": new_name, "genre": new_genre}})
            if result:
                output = {"name": name, "genre": new_genre}
                return {"result": output, "message": "Film created successfully!"}, 200
        return {"message": "Bad request parameters!"}, 400

    def delete(self, name):
        if films.find_one({"name": name}):
            films.delete_one({"name": name})
            return {"message": "record deleted"}, 200
        else:
            return {"message": "no record found"}, 404


@api.route('/genres')
class Genre(Resource):
    def get(self):
        output = []
        genres = films.distinct("genre")
        output.append({"genres": genres})
        return {"result": output}, 200


@api.route('/genres/<string:name>')
class FilmsOfSpecificGenre(Resource):
    def get(self, name):
        output = []
        for q in films.find({"genre": name}):
            output.append({"name": q["name"], "genre": q["genre"]})
        return {"result": output}, 200


@api.route('/voting')
class Voting(Resource):
    def get(self):
        output = []
        for q in voting.find():
            output.append({"name": q["name"], "films": [name for name in q["films"]]})
        return {"result": output}, 200

    def post(self):
        name = request.form["name"]
        name_films = request.form.getlist("films")
        if name and name_films:
            link = voting.insert_one({"name": name, "films": []})
            for name_film in name_films:
                voting.update({"name": name}, {"$push": {"films": {"name": name_film, "count": 0}}})
            output = "/voting/" + str(link.inserted_id)
            return {"result": output}, 200
        return {"message": "Bad request parameters!"}, 400


@api.route('/voting/<string:_id>')
class VotingItem(Resource):
    def get(self, _id):
        output = []
        voting_item = voting.find_one({"_id": ObjectId(_id)})
        if voting_item:
            output.append({"name": voting_item["name"], "films": [name for name in voting_item["films"]]})
            return {"result": output}, 200
        return {"message": "no record found"}, 404

    def put(self, _id):
        name = request.form["name"]
        if name:
            v_item = voting.update({"_id": ObjectId(_id), "films.name": name}, {"$inc": {"films.$.count": 1}})
            if v_item:
                return {"message": "Vote added successfully!"}, 200
            return {"message": "no record found"}, 404
        return {"message": "Bad request parameters!"}, 400

    def delete(self, _id):
        output = {}
        voting_item = voting.find_one({"_id": ObjectId(_id)})
        if voting_item:
            max = 0
            for name in voting_item["films"]:
                if max < name["count"]:
                    max = name["count"]
                    output.update({"winner": {"name": name["name"], "count": name["count"]}})
            id_v = history_of_voting.insert_one({"name": voting_item["name"], "winner": output["winner"],
                                                "films": [name for name in voting_item["films"]]}).inserted_id
            id_r = film_rating.insert_one({"history_of_voting": id_v,
                                           "name": output["winner"]["name"],
                                           "count": 0, "sum": 0}).inserted_id
            output["link to the rating"] = "film_rating/" + str(id_r)
            voting.delete_one({"_id": ObjectId(_id)})
            return output, 200
        return {"message": "no record found"}, 404


@api.route('/film_rating')
class Rating(Resource):
    def get(self):
        output = []
        for q in film_rating.find():
            output.append({"name": q["name"], "rating": q["sum"] / q["count"]})
        return {"result": output}, 200


@api.route('/film_rating/<string:_id>')
class RatingItem(Resource):
    def get(self, _id):
        output = []
        rating = film_rating.find_one({"_id": ObjectId(_id)})
        if rating:
            output.append({"name": rating["name"], "rating": round(rating["sum"] / rating["count"], 2)})
            return {"result": output}, 200
        return {"message": "no record found"}, 404

    def put(self, _id):
        rating = request.form["rating"]
        if rating:
            r_item = film_rating.update({"_id": ObjectId(_id)}, {"$inc": {"count": 1, "sum": int(rating)}})
            if r_item:
                return {"message": "Rating added successfully!"}, 200
            return {"message": "no record found"}, 404
        return {"message": "Bad request parameters!"}, 400

    def delete(self, _id):
        rating = film_rating.find_one({"_id": ObjectId(_id)})
        if rating:
            history_of_voting.update_one({"_id": rating["history_of_voting"]},
                                         {"$set": {"rating": round(rating["sum"] / rating["count"], 2)}})
            film_rating.delete_one({"_id": ObjectId(_id)})
            return {"message": "record deleted"}, 200
        return {"message": "no record found"}, 404


@api.route('/history')
class History(Resource):
    def get(self):
        output = []
        for q in history_of_voting.find():
            if q["rating"]:
                output.append({"name": q["name"], "winner": q["winner"],
                               "rating": q["rating"],
                               "films": [name for name in q["films"]]})
            else:
                output.append({"name": q["name"], "winner": q["winner"],
                               "films": [name for name in q["films"]]})
        return {"result": output}, 200


@api.route('/history/<string:_id>')
class HistoryItem(Resource):
    def get(self, _id):
        output = []
        history = history_of_voting.find_one({"_id": ObjectId(_id)})
        if history:
            if history["rating"]:
                output.append({"name": history["name"], "winner": history["winner"],
                               "rating": history["rating"],
                               "films": [name for name in history["films"]]})
            else:
                output.append({"name": history["name"], "winner": history["winner"],
                               "films": [name for name in history["films"]]})
            return {"result": output}, 200
        return {"message": "no record found"}, 404

    def delete(self, _id):
        if history_of_voting.find_one({"_id": ObjectId(_id)}):
            history_of_voting.delete_one({"_id": ObjectId(_id)})
            return {"message": "record deleted"}, 200
        else:
            return {"message": "no record found"}, 404
