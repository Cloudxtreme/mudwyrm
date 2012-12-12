from pyramid.view import view_config
from pyramid.httpexceptions import HTTPMovedPermanently

@view_config(route_name='root', permission='view')
def root(request):
    return HTTPMovedPermanently(request.route_url('games'))