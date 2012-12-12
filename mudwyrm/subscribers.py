from pyramid.events import subscriber, BeforeRender, NewRequest
from pyramid.i18n import get_localizer, TranslationStringFactory
from pyramid.httpexceptions import HTTPForbidden

from mudwyrm import helpers


_tsf = TranslationStringFactory('mudwyrm')

@subscriber(NewRequest)
def add_localizer(event):
    localizer = get_localizer(event.request)
    def auto_translate(string):
        return localizer.translate(_tsf(string))
    event.request.localizer = localizer
    event.request.translate = auto_translate
        
@subscriber(BeforeRender)
def add_renderer_globals(event):
    event['h'] = helpers
    if event['request']:
        event['_'] = event['request'].translate
        event['localizer'] = event['request'].localizer
    
@subscriber(NewRequest)
def csrf_validation(event):
    if event.request.method == "POST":
        token = event.request.POST.get("_csrf")
        if token is None or token != event.request.session.get_csrf_token():
            raise HTTPForbidden, "CSRF token is missing or invalid"