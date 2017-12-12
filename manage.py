import os

from flask_migrate import Migrate
from flask_socketio import SocketIO

from app import create_app
from app.database import db
from app.models import Message

socketio = SocketIO()

config_name = os.environ.get('FLASK_CONFIG') or 'default'
app = create_app(config_name)
migrate = Migrate(app, db)
socketio.init_app(app)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Message=Message)
