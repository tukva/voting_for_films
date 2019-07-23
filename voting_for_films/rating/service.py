from voting_for_films import ns_rating, col_rating, col_history
from bson.objectid import ObjectId


class RatingDAO(object):
    def __init__(self):
        self.rating = col_rating

    def get_all(self):
        output = []
        for q in col_rating.find():
            if q["count"] == 0:
                output.append({"name": q["name"]})
            else:
                output.append({"name": q["name"], "rating": round(q["sum"] / q["count"], 2)})
        return output

    def get_one(self, id):
        output = []
        r_item = col_rating.find_one({"_id": ObjectId(id)})
        if r_item:
            if r_item["count"] == 0:
                output.append({"name": r_item["name"]})
            else:
                output.append({"name": r_item["name"], "rating": round(r_item["sum"] / r_item["count"], 2)})
            return output
        ns_rating.abort(404, "Rating {} doesn't exist".format(id))

    def rate(self, id, data):
        rate = data.get("rate")
        r_item = col_rating.update({"_id": ObjectId(id)}, {"$inc": {"count": 1, "sum": int(rate)}})
        if r_item:
            return {"message": "Rating added successfully!"}
        ns_rating.abort(404, "Rating {} doesn't exist".format(id))

    def delete(self, id):
        r_item = col_rating.find_one({"_id": ObjectId(id)})
        if r_item:
            col_history.update_one({"_id": r_item["history_of_voting"]},
                               {"$set": {"rating": round(r_item["sum"] / r_item["count"], 2)}})
            col_rating.delete_one({"_id": ObjectId(id)})
            return {"message": "record deleted"}
        ns_rating.abort(404, "Rating {} doesn't exist".format(id))
