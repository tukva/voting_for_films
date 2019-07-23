from flask_restplus import Resource
from voting_for_films import ns_voting
from voting_for_films.voting.models import model_voting, name_fields, link_fields
from voting_for_films.voting.service import VotingDAO

votingDAO = VotingDAO()
@ns_voting.route('')
class VotingList(Resource):
    @ns_voting.marshal_list_with(model_voting, envelope='data')
    def get(self):
        return votingDAO.get_all(), 200

    @ns_voting.expect(model_voting, code=201)
    @ns_voting.marshal_list_with(link_fields)
    def post(self):
        return votingDAO.create(ns_voting.payload), 201


@ns_voting.response(404, 'Films not found')
@ns_voting.route('/<string:id>')
class Voting(Resource):
    @ns_voting.marshal_list_with(model_voting)
    def get(self, id):
        return votingDAO.get_one(id), 200

    @ns_voting.expect(name_fields)
    def patch(self, id):
        return votingDAO.cast_vote(id, ns_voting.payload), 200

    @ns_voting.marshal_list_with(link_fields)
    def delete(self, id):
        return votingDAO.delete(id), 200
