

from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse, fields, marshal,
                               marshal_with, url_for)


import models

phrase_fields = {
    'id': fields.Integer,
    'userId': fields.String,
    'phrase': fields.String,
    'text': fields.String,
    'setLanguage': fields.String,
    'transLanguage': fields.String

}


class PhraseList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument(
            'userId',
            required=False,
            help='No userId name provided',
            location=['form', 'json']
            )

        self.reqparse.add_argument(
            'phrase',
            required=False,
            help='No phrase name provided',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'text',
            required=False,
            help='No text name provided',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'setLanguage',
            required=False,
            help='No text name provided',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'transLanguage',
            required=False,
            help='No text name provided',

            location=['form', 'json']
            )
        super().__init__()
    
    
    def get(self):
  
        new_phrases = [marshal(phrase, phrase_fields) for phrase in models.Phrase.select()]
        
        return new_phrases

    @marshal_with(phrase_fields)
    def post(self):
        args = self.reqparse.parse_args() 
        phrase = models.Phrase.create(**args)
        return (phrase, 201)

class Phrase(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'userId',
            required=False,
            help='No userId name provided',
            location=['form', 'json']
            )

        self.reqparse.add_argument(
            'phrase',
            required=False,
            help='No phrase name provided',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'text',
            required=False,
            help='No text name provided',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'setLanguage',
            required=False,
            help='No text name provided',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'transLanguage',
            required=False,
            help='No text name provided',
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
        args = self.reqparse.parse_args()
        query = models.Phrase.update(**args).where(models.Phrase.id==id)
        query.execute()
        return (models.Phrase.get(models.Phrase.id==id), 204)

    def delete(self, id):
        query = models.Phrase.delete().where(models.Phrase.id == id)
        query.execute()
        return {"message": "resource deleted"}



phrases_api = Blueprint('resources.phrases', __name__)


api = Api(phrases_api)

api.add_resource(
    PhraseList,
    '/create',
    
)
api.add_resource(
    Phrase,
    '/<int:id>'
)