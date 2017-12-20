import os

from flask_migrate import Migrate
from flask_socketio import SocketIO
import click

from app import create_app
from app.database import db
from app.models import Message, User, Auth, Role

socketio = SocketIO()

config_name = os.environ.get('FLASK_CONFIG') or 'default'
app = create_app(config_name)
migrate = Migrate(app, db)
socketio.init_app(app)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Message=Message, User=User, Auth=Auth, Role=Role)


@app.cli.command()
@click.option('--username', help='Admin Username', prompt='Admin Username', type=(str))
@click.option('--email', help='Admin Email', prompt='Admin Email', type=(str))
@click.password_option('--password', help='Admin Password', prompt=True, confirmation_prompt=True, hide_input=True, type=(str))
def superuser(username: str, email: str, password: str):
    """Creates a super-user Account
    """
    username, email, password = map(str, (username, email, password))
    if not username or not email:
        click.echo(click.style('missing username or email {} {}'.format(type(username), type(email)), fg='red'))
        return
    role = Role.query.filter_by(name='Admin').first()
    user = User.query.filter_by(name=username).first()
    if user is not None:
        click.echo(click.style('Username Already in Use', fg='red'))
        return
    auth = Auth.query.filter_by(email=email).first()
    if auth:
        click.echo(click.style("Email already in Use!", fg='red'))
        return
    auth = Auth.create(email=email, password=password)
    user = User.create(name=username, auth=auth, role=role)
    click.echo(click.style('Super User created', fg='green'))
    return


@app.cli.command()
def deploy():
    """Run deployment tasks"""
    from flask_migrate import upgrade
    from app.models import Role
    # migrate database to latest revision
    click.echo(click.style("Perfoming Migrations .....", fg='green'))
    upgrade()
    # create user roles
    click.echo(click.style('Updating roles ....', fg='green'))
    Role.insert_roles()
    click.echo(click.style('Done ....', fg='green'))
    return
