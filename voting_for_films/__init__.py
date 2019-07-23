from flask import Flask, Blueprint
from flask_restplus import Api
from pymongo import MongoClient

blueprint = Blueprint('api', __name__)
api = Api(blueprint, version='1.0', title='VotingForFilmsMVC API', description='A simple VotingForFilmsMVC API', )
ns_films = api.namespace('films', description='Films operations')
ns_voting = api.namespace('voting', description='Voting operations')
ns_rating = api.namespace('rating', description='Rating operations')
ns_history = api.namespace('history', description='History operations')
app = Flask(__name__)
app.config['RESTPLUS_VALIDATE'] = True
app.register_blueprint(blueprint, url_prefix='/api/v1')
client = MongoClient("mongodb+srv://tukva:24121997tukva@cluster0-1jj3e.mongodb.net/test?retryWrites=true&w=majority")
db = client.voting_for_films

col_films = db.films
col_voting = db.voting
col_history = db.history_of_voting
col_rating = db.film_rating

from voting_for_films.films import views
from voting_for_films.voting import views
from voting_for_films.rating import views
from voting_for_films.history import views
