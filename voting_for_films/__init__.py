from flask import Flask
from flask_restplus import Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)
client = MongoClient("")
db = client.voting_for_films

films = db.films
films.create_index("name", unique=True)
voting = db.voting
history_of_voting = db.history_of_voting
film_rating = db.film_rating

from voting_for_films import routes
