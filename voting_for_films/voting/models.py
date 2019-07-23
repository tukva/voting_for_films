from voting_for_films import ns_voting
from flask_restplus import fields

choice_fields = ns_voting.model("Choice", {
    "name": fields.String(required=True, description='The name of the film'),
    "count": fields.Integer(readonly=True, default=0)
})

model_voting = ns_voting.model('Voting', {
    'name': fields.String(required=True, description='The name of the voting'),
    'films': fields.List(fields.Nested(choice_fields)),
    'current_votes': fields.Integer(readonly=True, default=0, description='Current votes of the voting'),
    'max_votes': fields.Integer(description='Max votes of the voting')
})

name_fields = ns_voting.model("Name", {
    "name": fields.String(required=True),
})

link_fields = ns_voting.model("Link", {
    "link": fields.String(required=True),
})
