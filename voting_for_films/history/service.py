from voting_for_films import ns_history, col_history
from bson.objectid import ObjectId


class HistoryDAO(object):
    def __init__(self):
        self.history = col_history

    def get_all(self):
        return list(col_history.find())

    def get_one(self, id):
        h_item = col_history.find_one({"_id": ObjectId(id)})
        if h_item:
            return h_item
        ns_history.abort(404, "History {} doesn't exist".format(id))

    def delete(self, id):
        if col_history.find_one({"_id": ObjectId(id)}):
            col_history.delete_one({"_id": ObjectId(id)})
            return {"message": "record deleted"}
        else:
            ns_history.abort(404, "History {} doesn't exist".format(id))
