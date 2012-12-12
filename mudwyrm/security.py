from pyramid.security import Allow, ALL_PERMISSIONS

from mudwyrm.models import DBSession
from mudwyrm.models.auth import User

DefaultAcl = [
    (Allow, 'group:users', ('view', 'play', 'edit')),
    (Allow, 'group:admins', ALL_PERMISSIONS),
]

def authentication_callback(userid, request):
    db = DBSession()
    user = db.query(User).filter(User.id==userid).first()
    if user:
        request.remote_user = user.name
        return [('group:%s' % group.name) for group in user.groups]
    else:
        request.remote_user = None
