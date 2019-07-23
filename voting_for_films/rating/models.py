from voting_for_films import ns_rating
from flask_restplus import fields

model_rating = ns_rating.model('Rating', {
    'name': fields.String(required=True, description='The name of the film'),
    'rating': fields.Float(description='The rating of the film')
})

rate_fields = ns_rating.model("Rate", {
    "rate": fields.Integer(required=True,  min=1, max=10, description='Film rating'),
})

