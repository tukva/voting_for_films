from flask import request
from flask_restplus import Resource
from voting_for_films import ns_films
from voting_for_films.films.models import model_film, genres_fields
from voting_for_films.films.service import FilmDAO

filmDAO = FilmDAO()
@ns_films.route('')
class FilmList(Resource):
    @ns_films.marshal_list_with(model_film, envelope='data')
    def get(self):
        return filmDAO.get_all(actor=request.args.get("actor"), genre=request.args.get("genre")), 200

    @ns_films.expect(model_film)
    @ns_films.marshal_list_with(model_film, code=201)
    def post(self):
        return filmDAO.create(ns_films.payload), 201


@ns_films.route('/<int:id>')
@ns_films.response(404, 'Films not found')
class Film(Resource):
    @ns_films.marshal_list_with(model_film)
    def get(self, id):
        return filmDAO.get_one(id), 200

    @ns_films.expect(model_film)
    @ns_films.marshal_list_with(model_film, code=201)
    def post(self, id):
        return filmDAO.create_with_id(id, ns_films.payload), 201

    @ns_films.expect(model_film)
    @ns_films.marshal_list_with(model_film)
    def put(self, id):
        return filmDAO.update(id, ns_films.payload), 200

    def delete(self, id):
        filmDAO.delete(id), 200


@ns_films.route('/genres')
class GenreList(Resource):
    @ns_films.marshal_list_with(genres_fields)
    def get(self):
        return filmDAO.get_genres(), 200
