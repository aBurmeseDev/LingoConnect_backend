

from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse, fields, marshal,
                               marshal_with, url_for)


import models

## define what fields we want on our responses

## Marshal Fields
# phrase_fields have to do with what we want the response object
# to the client to look like
phrase_fields = {
    'id': fields.Integer,
    'userId': fields.String,
    'phrase': fields.String
}

# view functions
class PhraseList(Resource):
    def __init__(self):
        # reqparse, its like body-parser in express, (it makes the request object's body readable)
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument(
            'name',
            required=False,
            help='No phrase name provided',
            location=['form', 'json']
            )

        self.reqparse.add_argument(
            'breed',
            required=False,
            help='No phrase name provided',
            location=['form', 'json']
            )

        self.reqparse.add_argument(
            'owner',
            required=False,
            help='No phrase name provided',
            location=['form', 'json']
            )

        super().__init__()
    
    
    def get(self):
        # models.Phrase.select() ## Look up peewee queries
        # all_phrases = models.Phrase.select()
        # print(all_phrases, "<--- all phrases result of db.query")
        # new_phrases = []

        # for phrase in all_phrases:
        #     new_phrases.append(marshal(phrase, phrase_fields))

        new_phrases = [marshal(phrase, phrase_fields) for phrase in models.Phrase.select()]
        # [{}, Model Instances]
        # for Generating response object
        # marshal in flask
        return new_phrases

    @marshal_with(phrase_fields)
    def post(self):
        # read the args "req.body"
        args = self.reqparse.parse_args() # body-parser
        print(args, '<----- args (req.body)')
        phrase = models.Phrase.create(**args)
        user = g.user._get_current_object()

        print(phrase, "<---" , type(phrase))
        # line 52 does line 54
        # phrase = models.Phrase.create(name=args['name'], breed=args['breed'], owner=args['owner'])
        return (phrase, 201)

class Phrase(Resource):
    def __init__(self):
        # reqparse, its like body-parser in express, (it makes the request object's body readable)
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument(
            'name',
            required=False,
            help='No phrase name provided',
            location=['form', 'json']
            )

        self.reqparse.add_argument(
            'breed',
            required=False,
            help='No phrase name provided',
            location=['form', 'json']
            )

        self.reqparse.add_argument(
            'owner',
            required=False,
            help='No phrase name provided',
            location=['form', 'json']
            )

        super().__init__()

    @marshal_with(phrase_fields)
    def get(self, id):

        try:
            phrase = models.Phrase.get(models.Phrase.id==id)
        except models.Phrase.DoesNotExist:
            abort(404)
        else:
            return (phrase, 200)

    @marshal_with(phrase_fields)
    def put(self, id):
        # parse the args (get req.body)
        args = self.reqparse.parse_args()
        query = models.Phrase.update(**args).where(models.Phrase.id==id)
        # we have execute the query
        query.execute()
        print(query, "<--- this is query")
        # the query doesn't respond with the update object
        return (models.Phrase.get(models.Phrase.id==id), 204)

    def delete(self, id):
        query = models.Phrase.delete().where(models.Phrase.id == id)
        query.execute()
        return {"message": "resource deleted"}


# were setting a module of view functions that can be attached to our flask app
phrases_api = Blueprint('resources.phrases', __name__)
#module.exports = controller

#instatiating our api from the blueprint
# gives us the special methods we can operate our api with
api = Api(phrases_api)

api.add_resource(
    PhraseList,
    '/phrases'
)
api.add_resource(
    Phrase,
    '/phrases/<int:id>'
)