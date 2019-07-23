from voting_for_films import ns_history
from flask_restplus import fields

choice_fields = ns_history.model("Choice", {
    "name": fields.String(required=True, description='The name of the film'),
    "count": fields.Integer(readonly=True, default=0)
})
model_history = ns_history.model('History', {
    'name': fields.String(required=True, description='The name of the voting'),
    'winner': fields.String(required=True, description='The winner of the voting'),
    'films': fields.List(fields.Nested(choice_fields)),
    'rating': fields.Float(description='The rating of the film')
})
