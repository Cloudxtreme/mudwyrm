from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.security import forget
from pyramid.security import authenticated_userid
from pyramid.url import route_url
from pyramid.view import view_config
from pyramid.exceptions import Forbidden
import transaction
import formencode
from formencode import validators

from mudwyrm.models import DBSession, MAX_STR_LENGTH
from mudwyrm.models.auth import User, Group
from mudwyrm.forms import Schema, Form, FormRenderer

def passwords_match(value, field):
    if field.parent.password.value != value:
        raise validators.ValidationError(u"Passwords do not match")
        
class LoginSchema(Schema):
    name = validators.MaxLength(MAX_STR_LENGTH)
    password = validators.MaxLength(MAX_STR_LENGTH)
        
class UniqueUsername(formencode.FancyValidator):
    def _to_python(self, value, state):
        db = DBSession()
        user = db.query(User.id).filter(User.name == value).first()
        if user:
            raise formencode.Invalid("That username is already taken",
                                     value, state)
        return value
    
class RegistrationSchema(Schema):
    name = formencode.All(
        validators.MaxLength(MAX_STR_LENGTH, not_empty=True),
        UniqueUsername())
    password = formencode.All(
        validators.MaxLength(MAX_STR_LENGTH),
        validators.MinLength(6))
    password_confirmation = validators.String()
    email = validators.Email(not_empty=True)
    chained_validators = [
        validators.FieldsMatch('password', 'password_confirmation')]


@view_config(name='login',
             renderer='mudwyrm:templates/auth/login.mako')
def login(request):
    came_from = request.params.get('came_from', '/')
    auth_failed = False
    form = Form(request, LoginSchema)
    if form.validate():
        db = DBSession()
        user = db.query(User).filter(User.name == form.data['name']).first()
        if user and user.validate_password(form.data['password']):
            return HTTPFound(location=came_from,
                             headers=remember(request, user.id))
        auth_failed = True
    return dict(
        auth_failed = auth_failed,
        form = FormRenderer(form)
    )

@view_config(name='logout')
def logout(request):
    request.remote_user = None
    return HTTPFound('/', headers=forget(request))
 
@view_config(renderer='mudwyrm:templates/auth/forbidden.mako',
             context=Forbidden)
def forbidden(request):
    if not authenticated_userid(request):
        return HTTPFound('/login?came_from=%s' % request.url)
    return {}

@view_config(name='register',
             renderer='mudwyrm:templates/auth/register.mako')
def register(request):
    db = DBSession()
    form = Form(request, RegistrationSchema)
    if form.validate():
        user = form.bind(User(), exclude=['password_confirmation'])
        group = db.query(Group).filter(Group.name == 'users').one()
        user.groups.append(group)
        db.add(user)
        db.flush()
        transaction.commit()
        return HTTPFound(location=request.route_url('root'))
    return dict(form=FormRenderer(form))