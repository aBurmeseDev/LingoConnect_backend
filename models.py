import datetime

# peewee is arm
# this will give our model the power to talk to postgres sql
# peewee is kinda mongoose
from peewee import *
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin


DATABASE = PostgresqlDatabase('dogs', user='johnuser', password='momo')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        email = email.lower()
        try:
            cls.select().where(
                cls.email == email
            ).get()
        except cls.DoesNotExist:
            # we are instatiting an instance of the class
            user = cls(username=username, email=email)
            # pushing our password with bcrypt
            user.password = generate_password_hash(password)
            # save puts the user in the db
            user.save()
            return user
        else:
            raise Exception('user with that email already exists')


class Dog(Model):
    name = CharField()
    owner = CharField()
    breed = CharField()
    created_by = ForeignKeyField(User, related_name='dog_set')
    created_at = DateTimeField(default=datetime.datetime.now)
    # instructions on what database to connect too, in our current case splite

    class Meta:
        # instructions on what database to connect to
        database = DATABASE


def initialize():
    DATABASE.connect()  # opening a connection to the db
    # the array takes our models and will create tables that match y
    DATABASE.create_tables([User, Dog], safe=True)
    DATABASE.close()
