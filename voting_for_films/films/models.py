from voting_for_films import ns_films
from flask_restplus import fields


model_film = ns_films.model('Film', {
    'id': fields.Integer(readonly=True, description='The film unique identifier'),
    'name': fields.String(required=True, description='The name of the film'),
    'genres': fields.List(fields.String(), required=True, description='The genres of the film'),
    'actors': fields.List(fields.String(), required=True, description='The cast of the film')
})

genres_fields = ns_films.model("Genres", {
    'genres': fields.List(fields.String(), required=True, description='The genres of the film')
})
