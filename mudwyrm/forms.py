import formencode
from pyramid_simpleform import Form, State
from pyramid_simpleform.renderers import FormRenderer

class Schema(formencode.Schema):
    filter_extra_fields = True
    allow_extra_fields = True
    
