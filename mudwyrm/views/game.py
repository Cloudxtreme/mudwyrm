from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.security import authenticated_userid
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
import transaction
import os
import shutil
import formencode
from formencode import validators

from mudwyrm.models import DBSession, MAX_STR_LENGTH
from mudwyrm.models.auth import User
from mudwyrm.models.game import Game
from mudwyrm.forms import Schema, Form, FormRenderer, State

class UniqueGameName(formencode.FancyValidator):
    def _to_python(self, value, state):
        db = DBSession()
        game = db.query(Game.name).filter(
            Game.user_id == state.user_id).filter(Game.name == value).first()
        if game:
            raise formencode.Invalid("A game with that name already exists",
                                     value, state)
        return value

class AddGameSchema(Schema):
    name = formencode.All(
        validators.MaxLength(MAX_STR_LENGTH, not_empty=True),
        UniqueGameName())
    address = validators.MaxLength(MAX_STR_LENGTH, not_empty=True)
    port = validators.Int(not_empty=True)
    
class EditGameSchema(AddGameSchema):
    name = validators.String()

@view_config(route_name='games', renderer='mudwyrm:templates/game/games.mako',
             permission='view')
@view_config(route_name='games_json', renderer='json',
             permission='view')
def games(request):
    db = DBSession()
    user_id = authenticated_userid(request)
    games = db.query(Game.name).filter(Game.user_id == user_id).all()
    games = map(lambda g: g[0], games)
    return dict(games=games)

@view_config(route_name='play', permission='play')
def play(request):
    user_id = authenticated_userid(request)
    if user_id is None:
        return HTTPForbidden()
    username = request.remote_user
    gamename = request.matchdict['game']
    db = DBSession()
    game = db.query(Game.name).filter(Game.user_id == user_id).filter(
        Game.name == gamename).first()
    if not game:
        return HTTPNotFound(request.translate("That game doesn't exist."))
    return render_to_response(
        'mudwyrm_users:%s/%s/ui/templates/index.mako' % (username, gamename),
        {'user_files_url': '/user/%s/%s/' % (username, gamename)},
        request)

@view_config(route_name='add_game', renderer='mudwyrm:templates/game/add.mako',
             permission='edit')
def add(request):
    user_id = authenticated_userid(request)
    form = Form(request, AddGameSchema, state=State(user_id=user_id),
                defaults=dict(port=23))
    if form.validate():
        game = form.bind(Game())
        game.user_id = user_id
        db = DBSession()
        db.add(game)
        db.flush()
        transaction.commit()
        
        #template_dir = os.path.join(os.path.dirname(__file__),
        #                            '_game_session_template')
        #session_dir = os.path.join(self.users_dir, metauser.name, session.name)
        #if not os.path.exists(session_dir):
        #    shutil.copytree(template_dir, session_dir)
        
        return HTTPFound(location=request.route_url('games'))
    return dict(form=FormRenderer(form))

@view_config(route_name='edit_game', renderer='mudwyrm:templates/game/edit.mako',
             permission='edit')
def edit(request):
    name = request.matchdict['game']
    user_id = authenticated_userid(request)
    db = DBSession()
    game = db.query(Game).filter(
        Game.user_id == user_id).filter(Game.name == name).first()
    if not game:
        return HTTPNotFound(request.translate("A game named %s doesn't exist" % name))
    form = Form(request, EditGameSchema, obj=game)
    if form.validate():
        form.bind(game, exclude=['name'])
        transaction.commit()
        return HTTPFound(location=request.route_url('games'))
    return dict(form=FormRenderer(form))
