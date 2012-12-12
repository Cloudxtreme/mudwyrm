from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import String, Unicode, UnicodeText, Integer, DateTime, \
                             Boolean, Float
from sqlalchemy.orm import relation, backref, synonym

import os
from hashlib import sha1
from datetime import datetime

from mudwyrm.models import Base, MAX_STR_LENGTH


user_group_table = Table('user_groups', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('group_id', Integer, ForeignKey('groups.id',
        onupdate="CASCADE", ondelete="CASCADE"))
)

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(MAX_STR_LENGTH), unique=True, nullable=False)
    
    def __init__(self, name=None):
        self.name = name
    
    def __unicode__(self):
        return self.name

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(MAX_STR_LENGTH), unique=True, nullable=False)
    _password = Column('password', Unicode(MAX_STR_LENGTH), nullable=False)
    email = Column(Unicode(MAX_STR_LENGTH), nullable=False)
    
    groups = relation('Group', secondary=user_group_table, backref='users')
    
    def __init__(self, name=None, password=None, email=None, groups=[]):
        self.name = name
        self.password = password
        self.email = email
        self.groups.extend(groups)

    def _set_password(self, password):
        """Hash password on the fly."""
        if not password:
            self._password = u''
            return
        
        hashed_password = password

        if isinstance(password, unicode):
            password_mb = password.encode('UTF-8')
        else:
            password_mb = password

        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update(password_mb + salt.hexdigest())
        hashed_password = salt.hexdigest() + hash.hexdigest()

        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('UTF-8')

        self._password = hashed_password

    def _get_password(self):
        """Return the password hashed"""
        return self._password

    password = synonym('_password', descriptor=property(_get_password,
                                                        _set_password))

    def validate_password(self, password):
        """
        Check the password against existing credentials.

        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        :type password: unicode object.
        :return: Whether the password is valid.
        :rtype: bool
        """
        hashed_pass = sha1()
        hashed_pass.update(password + self.password[:40])
        return self.password[40:] == hashed_pass.hexdigest()
        
    def __unicode__(self):
        return self.name

