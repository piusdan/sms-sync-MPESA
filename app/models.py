from flask import abort
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .database import db
from .database.utils import CRUDMixin
from .utils import parse_message, kenyatime


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
