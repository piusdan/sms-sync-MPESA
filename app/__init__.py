from flask import Flask
from flask_moment import Moment
from flask_redis import FlaskRedis

from config import CONFIG
from .database import db

redis = FlaskRedis()
moment = Moment()


def create_app(config_name):
    '''Application factory to initialise and configure the application'''
    app = Flask(__name__)
    app.config.from_object(CONFIG[config_name])
    CONFIG[config_name].init_app(app)

    # intialise a database connection instance
    db.init_app(app)

    # intialize redis
    redis.init_app(app)

    # intialize flask moment for formating of datetimes
    moment.init_app(app)

    # register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    return app
