from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension
import transaction

MAX_STR_LENGTH = 80

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

def _populate():
    from mudwyrm.models.auth import User, Group
    db = DBSession()
    groups = { g[0]: Group(*g)
        for g in [(u'admins',),
                  (u'users',),
                 ]
    }
    for g in groups.values():
        db.add(g)
    users = { u[0]: User(*u)
        for u in [(u'admin', u'admin', u'admin@localhost', [groups[u'admins']]),
                  (u'user',  u'user',  u'user@localhost', [groups[u'users']]),
                 ]
    }
    for u in users.values():
        db.add(u)
    from mudwyrm.models.game import Game
    g = Game()
    g.name = u'achaea'
    g.address = u'achaea.com'
    g.port = 23
    g.user = users[u'admin']
    db.add(g)
    db.flush()
    transaction.commit()

def populate_data():
    try:
        _populate()
    except IntegrityError:
        DBSession.rollback()
    
def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
