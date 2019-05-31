import datetime
from peewee import *
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin


DATABASE = PostgresqlDatabase('phrases', user='josh', password='karp')


class User(UserMixin, Model):
    username = CharField()
    email = CharField(unique=True)
    password = CharField()
    primaryLanguage = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, primaryLanguage, **kwargs):
        email = email.lower()
        try:
            cls.select().where(
                cls.email == email
            ).get()
        except cls.DoesNotExist:
            user = cls(username=username, email=email, primaryLanguage=primaryLanguage)
            user.password = generate_password_hash(password)
            user.save()
            return user
        else:
            raise Exception('user with that email already exists')


class Phrase(Model):
    userId = CharField()
    text = CharField()
    phrase = CharField()
    setLanguage = CharField()
    transLanguage = CharField()



    class Meta:
        
        database = DATABASE


def initialize():
    DATABASE.connect() 
    DATABASE.create_tables([User, Phrase], safe=True)
    DATABASE.close()
