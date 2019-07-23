from flask_restplus import Resource
from voting_for_films import ns_history
from voting_for_films.history.models import model_history
from voting_for_films.history.service import HistoryDAO

historyDAO = HistoryDAO()
@ns_history.route('')
class HistoryList(Resource):
    @ns_history.marshal_list_with(model_history)
    def get(self):
        return historyDAO.get_all(), 200


@ns_history.route('/<string:id>')
class History(Resource):
    @ns_history.marshal_list_with(model_history)
    def get(self, id):
        return historyDAO.get_one(id), 200

    def delete(self, id):
        return historyDAO.delete(id), 200
