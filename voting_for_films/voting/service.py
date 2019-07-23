from voting_for_films import ns_films, ns_voting, col_voting, col_history, col_rating
from bson.objectid import ObjectId


class VotingDAO(object):
    def __init__(self):
        self.voting = col_voting

    def get_all(self):
        return list(col_voting.find())

    def get_one(self, id):
        v_item = col_voting.find_one({"_id": ObjectId(id)})
        if v_item:
            return v_item
        ns_films.abort(404, "Voting {} doesn't exist".format(id))

    def create(self, data):
        max_votes = data.get("max_votes")
        if max_votes and max_votes > 0:
            data["current_votes"] = 0
            _id = col_voting.insert_one(data).inserted_id
        else:
            data.pop("max_votes")
            _id = col_voting.insert_one(data).inserted_id
        for film in data["films"]:
            col_voting.update({"_id": _id, "films.name": film["name"]}, {"$set": {"films.$.count": 0}})
        output = "/voting/" + str(_id)
        return {"link": output}

    def cast_vote(self, id, data):
        name = data.get("name")
        v_item = col_voting.find_one({"_id": ObjectId(id)})
        if v_item:
            if "max_votes" in v_item:
                if v_item["max_votes"] > v_item["current_votes"]:
                    vote = col_voting.update({"_id": ObjectId(id), "films.name": name},
                                         {"$inc": {"films.$.count": 1, "current_votes": 1}})
                    if not vote:
                        ns_voting.abort(404, "Bad request parameters!")
                else:
                    ns_voting.abort(404, "You can't vote because the voting closed!")
            else:
                col_voting.update({"_id": ObjectId(id), "films.name": name}, {"$inc": {"films.$.count": 1}})
            return {"message": "Vote added successfully!"}
        ns_voting.abort(404, "Voting {} doesn't exist".format(id))

    def delete(self, id):
        output = {}
        voting_item = col_voting.find_one({"_id": ObjectId(id)})
        if voting_item:
            max = 0
            for name in voting_item["films"]:
                if max < name["count"]:
                    max = name["count"]
                    output.update({"winner": {"name": name["name"], "count": name["count"]}})
            id_v = col_history.insert_one({"name": voting_item["name"], "winner": output["winner"],
                                       "films": voting_item["films"]}).inserted_id
            id_r = col_rating.insert_one({"history_of_voting": id_v,
                                      "name": output["winner"]["name"],
                                      "count": 0, "sum": 0}).inserted_id
            output["link"] = "film_rating/" + str(id_r)
            col_voting.delete_one({"_id": ObjectId(id)})
            return output
        ns_voting.abort(404, "Voting {} doesn't exist".format(id))
