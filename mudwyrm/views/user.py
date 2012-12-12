from pyramid.view import view_config
from pyramid.exceptions import Forbidden, NotFound
from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid
from pyramid.renderers import render_to_response
from pyramid.static import static_view

from mudwyrm.models import DBSession
from mudwyrm.models.auth import User
from mudwyrm.security import DefaultAcl

import pkg_resources
import os

def user_files_dir(user_name):
    return pkg_resources.resource_filename('mudwyrm_users', user_name)

class UserFiles(object):
    __acl__ = DefaultAcl
    
    def __init__(self, name, parent, path, root_dir):
        self.__name__ = name
        self.__parent__ = parent
        self.path = path
        self.root_dir = root_dir
        self.is_dir = os.path.isdir(self.path)
    
    def __getitem__(self, name):
        if not self.is_dir:
            raise KeyError()
        child_path = os.path.normpath(os.path.join(self.path, name))
        if not child_path.startswith(self.root_dir):
            raise KeyError()
        if not os.path.exists(child_path):
            raise KeyError()
        return UserFiles(name, self, child_path, self.root_dir)

def user_factory(request):
    user_name = request.matchdict['user_name']
    root_dir = user_files_dir(user_name)
    return UserFiles('', None, root_dir, root_dir)

def _authenticated_user(request):
    user_name = request.matchdict['user_name']
    db = DBSession()
    user = db.query(User).filter(
            User.name == user_name).first()
    if not user or user.id != authenticated_userid(request):
        return None
    return user
    
@view_config(route_name='user', name='', permission='view')
@view_config(route_name='user', name='view', permission='view')
def view(context, request):
    user = _authenticated_user(request)
    if not user:
        return Forbidden()
    request_ = request.copy()
    request_.path_info = os.path.join(*request.traversed)
    sv = static_view(user.name, package_name='mudwyrm_users')
    return sv(context, request_)
    
@view_config(route_name='user', name='list', permission='view')
def list(context, request):
    user = _authenticated_user(request)
    if not user:
        return Forbidden()
    if not context.is_dir:
        return NotFound()
    filelist = []
    for name in os.listdir(context.path):
        path = os.path.join(context.path, name)
        dir_url = request.path.rpartition('/')[0] + '/' + name
        filelist.append(dict(
            name = name,
            path = dir_url,
            type = 'dir' if os.path.isdir(path) else 'file',
        ))
    filelist.sort(key=lambda file: file['type'])
    return render_to_response('json', filelist, request)

@view_config(route_name='user', name='add', renderer='json', permission='edit')
def add(request):
    user = _authenticated_user(request)
    if not user:
        return Forbidden()

@view_config(route_name='user', name='edit', request_method='POST',
             renderer='json', permission='edit')
def edit_post(context, request):
    user = _authenticated_user(request)
    if not user:
        return Forbidden()
    user_dir = user_files_dir(user.name) 
    file_path = os.path.normpath(os.path.join(user_dir, *request.traversed))
    if not file_path.startswith(user_dir):
        return NotFound()
    contents = request.POST['contents']
    with open(file_path, 'wb') as file:
        file.write(contents)
    return {}
    
@view_config(route_name='user', name='edit',
             renderer='mudwyrm:templates/game/editor.mako', permission='edit')
def edit_get(context, request):
    user = _authenticated_user(request)
    if not user:
        return Forbidden()
    return dict(
        user_name = user.name,
        file_path = request.path.rpartition('/')[0]
    )
    
@view_config(route_name='user', name='delete', renderer='json',
             permission='edit')
def delete(request):
    user = _authenticated_user(request)
    if not user:
        return Forbidden()
