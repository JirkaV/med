from django.template.response import TemplateResponse

def response(request, template, extra_context=None, content_type=None, **kwargs):
    '''copy of django.views.generic.simple that returns 
    TemplateResponse instead of HttpResponse, so the context
    can be inspected by middleware just before the template is rendered.
    
    Useful for setting some "last minute" variables in the response
    middleware. Value of those would typically depend on something
    in the current context (and hence the need for the context analysis). 
    '''
    if extra_context is None: 
        extra_context = {}
    context_dict = {'params': kwargs}
    for key, value in extra_context.items():
        if callable(value):
            context_dict[key] = value()
        else:
            context_dict[key] = value
    return TemplateResponse(request, template, context_dict, content_type=content_type)
