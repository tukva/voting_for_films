from flask_restplus import Resource
from voting_for_films import ns_rating
from voting_for_films.rating.models import model_rating, rate_fields
from voting_for_films.rating.service import RatingDAO

ratingDAO = RatingDAO()
@ns_rating.route('')
class RatingList(Resource):
    @ns_rating.marshal_list_with(model_rating)
    def get(self):
        return ratingDAO.get_all(), 200


@ns_rating.route('/<string:id>')
class Rating(Resource):
    @ns_rating.marshal_list_with(model_rating)
    def get(self, id):
        return ratingDAO.get_one(id), 200

    @ns_rating.expect(rate_fields)
    def patch(self, id):
        return ratingDAO.rate(id, ns_rating.payload), 200

    def delete(self, id):
        return ratingDAO.delete(id), 200
