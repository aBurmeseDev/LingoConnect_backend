import datetime

# peewee is arm
# this will give our model the power to talk to postgres sql
# peewee is kinda mongoose
from peewee import *
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin


DATABASE = PostgresqlDatabase('phrases', user='johnuser', password='momo')


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
    phrase = CharField()
    created_by_user_id = ForeignKeyField(User, related_name='phrase_set')
    created_at = DateTimeField(default=datetime.datetime.now)
    # instructions on what database to connect too, in our current case splite

    class Meta:
        # instructions on what database to connect to
        database = DATABASE


def initialize():
    DATABASE.connect()  # opening a connection to the db
    # the array takes our models and will create tables that match y
    DATABASE.create_tables([User, Phrase], safe=True)
    DATABASE.close()
