
from flask import Flask, g
import models
from flask_cors import CORS
import config
from flask_login import LoginManager
from resources.users import users_api

DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


# app.use(dogControllr, '/api/v1')
# url prefix star

CORS(users_api, origins=["http://localhost:3002"], supports_credentials=True)

app.register_blueprint(users_api, url_prefix='/users')


@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/')
def index():
    return 'HIT'


if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)
