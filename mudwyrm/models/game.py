from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import relation, backref

import datetime

from mudwyrm.models import Base, MAX_STR_LENGTH
from mudwyrm.models.auth import User


def _now():
    return datetime.datetime.now()

class Game(Base):
    __tablename__ = 'games'
    id      = Column(Integer, primary_key=True, autoincrement=True)
    name    = Column(Unicode(MAX_STR_LENGTH), nullable=False)
    created = Column(DateTime, default=_now)
    address = Column(Unicode(1024), default=u'')
    port    = Column(Integer, default=23)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    user = relation(User, primaryjoin=User.id==user_id, backref='games')