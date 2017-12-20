from flask import Flask
from flask_moment import Moment
from flask_redis import FlaskRedis
from flask_socketio import SocketIO, emit
from flask_login import LoginManager


from config import CONFIG
from .database import db

redis = FlaskRedis()
moment = Moment()
socketio = SocketIO()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_message_category = 'warning'
login_manager.login_view = 'auth.login'


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

    # intialise socket IO
    socketio.init_app(app)

    # initialise login Manager
    login_manager.init_app(app)

    # register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .callbacks import callback as callback_blueprint
    app.register_blueprint(callback_blueprint, url_prefix='/callbacks')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
