# coding:utf-8
from django.middleware.csrf import get_token
from django.template import RequestContext
from django.conf import settings
from django.template.context import Context
from django.http import HttpResponse
from mako.lookup import TemplateLookup


def rander_to_response(request, template, data=None):
    context_instance = RequestContext(request)
    path = settings.TEMPLATES[0]['DIRS'][0]
    lookup = TemplateLookup(
        directories=[path],
        output_encoding='utf-8',
        input_encoding='utf-8'
    )
    mako_template = lookup.get_template(template)
    if not data:
        data = {}
    if context_instance:
        context_instance.update(data)
    else:
        context_instance = Context(data)
    result = {}
    for d in context_instance:
        result.update(d)
    result['request'] = request
    request.META["CSRF_COOKIE"] = get_token(request)
    result['csrf_token'] = ('<div style="display:none">'
                            '<input type="hidden" '
                            'name="csrfmiddlewaretoken" '
                            'value="{0}"/>'
                            '</div>'.format(request.META["CSRF_COOKIE"]))
    return HttpResponse(mako_template.render(**result))
# '<input type="hidden" name = "csrfmiddlewaretoken" value = "{0}" />'.format(
#         request.META.get('CSRF_COOKIE'))
