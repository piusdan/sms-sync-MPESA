from flask import abort, current_app
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import hashlib
from .database import db
from .database.utils import CRUDMixin
from .utils import parse_message, kenyatime


class Role(db.Model, CRUDMixin):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(12), nullable=False)
    default = Column(Boolean, default=False, index=True)
    permisions = Column(Integer)
    users = relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():

        roles = {
            'User': [Permission.READ, Permission.WRITE],
            'Moderator': [Permission.WRITE, Permission.READ, Permission.MODERATE],
            'Admin': [Permission.WRITE, Permission.READ, Permission.MODERATE, Permission.ADMINISTER]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role.create(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            role.save()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class Permission:
    READ = 1
    WRITE = 2
    MODERATE = 8
    ADMINISTER = 16


class User(UserMixin, db.Model, CRUDMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    phoneNumber = Column(String(14))
    auth_id = Column(Integer, ForeignKey('auth.id'))
    auth = relationship('Auth', back_populates="user", uselist=False)
    role_id = Column(Integer, ForeignKey('roles.id'))
    avatar_hash = Column(String)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.auth.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(name='Admin').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.auth.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    @staticmethod
    def reset_password(token, password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception as exc:
            return False
        id = data.get('reset')
        user = User.query.get(id)
        if user is None:
            return False
        user.auth.password = password
        user.save()
        return user

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def gravatar_hash(self):
        return hashlib.md5(self.auth.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)



class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


class Auth(db.Model, CRUDMixin):
    __tablename__ = 'auth'
    id = Column(Integer, primary_key=True)
    confirmed = Column(Boolean, default=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String)
    user = relationship('User', back_populates="auth", uselist=False)

    @property
    def password(self):
        return AttributeError("Password is not a readable property")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Customer(db.Model, CRUDMixin):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    phoneNumber = Column(String, nullable=False, unique=True)
    account_no = Column(String, nullable=False, unique=True)
    messages = relationship('Message', lazy='dynamic', backref='customer')


class Message(db.Model, CRUDMixin):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    text = Column(String(255), index=True)
    from_ = Column(String)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    to_ = Column(String)
    seen = Column(Boolean, default=False)
    seen_on = Column(DateTime, default=kenyatime)
    processed_on = Column(DateTime)

    sent_on = Column(DateTime, default=kenyatime)
    timestamp = Column(DateTime, default=kenyatime)

    def to_dict(self):
        return parse_message(self.text)

    @staticmethod
    def by_code(uuid):
        return Message.query.filter_by(code=uuid).first()

    @staticmethod
    def by_id(id):
        message = Message.query.get(id)
        if message is None:
            return abort(404)
        return message


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
