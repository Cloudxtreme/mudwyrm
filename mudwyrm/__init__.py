from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import engine_from_config
import pyramid_beaker

from mudwyrm.models import initialize_sql, populate_data
from mudwyrm.security import authentication_callback, DefaultAcl

class RootFactory(object):
   __acl__ = DefaultAcl
   def __init__(self, request):
      pass

def main(global_config, **settings):
    authentication_policy = AuthTktAuthenticationPolicy(
        settings['auth.secret'], callback=authentication_callback)
    authorization_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings,
            root_factory=RootFactory,
            authentication_policy=authentication_policy,
            authorization_policy=authorization_policy)
    
    config.scan()
    
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    populate_data()
    
    config.add_translation_dirs('mudwyrm:locale')
    
    session_factory = pyramid_beaker.session_factory_from_settings(settings)
    config.set_session_factory(session_factory)
    
    config.add_static_view('img', 'mudwyrm:static/img')
    config.add_static_view('css', 'mudwyrm:static/css')
    config.add_static_view('js', 'mudwyrm:static/js')
    
    config.add_route('user', '/user/{user_name}/*traverse',
                     factory='mudwyrm.views.user.user_factory')
    
    config.add_route('root', '/')
    config.add_route('games', '/games')
    config.add_route('games_json', '/games', accept='application/json')
    config.add_route('play', '/play/{game}')
    config.add_route('add_game', '/add')
    config.add_route('edit_game', '/edit/{game}')

    return config.make_wsgi_app()
