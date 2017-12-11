from flask import abort
from sqlalchemy import Column, Integer, String, DateTime

from .database import db
from .database.utils import CRUDMixin
from .utils import parse_message, kenyatime


class Message(db.Model, CRUDMixin):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    text = Column(String(255), index=True)
    from_ = Column(String)
    to_ = Column(String)
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
