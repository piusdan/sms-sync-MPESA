from flask import abort
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager

from .database import db
from .database.utils import CRUDMixin
from .utils import parse_message, kenyatime


class Role(db.Model, CRUDMixin):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(12), nullable=False)


class User(db.Model, CRUDMixin, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    phoneNumber = Column(String(14), unique=True, nullable=False)
    auth_id = Column(Integer, ForeignKey('auth.id'))
    auth = relationship('Auth', back_populates="user", uselist=False)

class AnonymousUser(AnonymousUserMixin):
    pass

login_manager.anonymous_user = AnonymousUser


class Auth(db.Model, CRUDMixin):
    __tablename__ = 'auth'
    id = Column(Integer, primary_key=True)
    confirmed = Column(Boolean, default=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String)
    user = relationship('user', back_populates="auth")

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
    phoneNumber = Column(String, nullable=False, unique=True, index=True)
    account_no = Column(String, nullable=False, unique=True, index=True)
    messages = relationship('Message', lazy='dynamic', backref='customer')


class Message(db.Model, CRUDMixin):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    text = Column(String(255), index=True)
    from_ = Column(String)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    to_ = Column(String)
    seen  = Column(Boolean, default=False)
    seen_on = Column(DateTime, default=kenyatime)
    processed_on = Column(DateTime)

    sent_on = Column(DateTime, default=kenyatime)
    timestamp = Column(DateTime,default=kenyatime)

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
def load_user(id):
    User.query.get(int(id))