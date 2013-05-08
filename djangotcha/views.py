from django.http import HttpResponseNotFound
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.conf import settings
from django.utils import translation
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

# Decorators
def templatable_view(template_name):
    def decorator(view):
        def wrapped_view(request, *a ,**kw):
            result = view(request, *a, **kw)
            lang = translation.get_language()

            # current_url = resolve(request.path_info).url_name
            context = {
                'request': request,
                'page': view.__name__,
                'page_canonical_url': '%(protocol)s://%(domain)s%(relative_url)s' % {'protocol': request.is_secure() and 'https' or 'http',
                                                                            'domain': request.META['HTTP_HOST'],
                                                                        'relative_url': request.path_info}

            }
            context.update(result)

            template = template_name + '.html'
            return render_to_response(template, context, context_instance=RequestContext(request))
        return wrapped_view
    return decorator

# Views
@templatable_view('home')
def home(request):
    return {}

@login_required
@templatable_view('profile')
def profile(request):
    return {}

@templatable_view('login')
def login(request):
    return {}

@templatable_view('authorized')
def authorized(request):
    return {}



@templatable_view('404')
def error404(request):
    return {}

@templatable_view('500')
def error500(request):
    raise Exception('Dummy internal server error')
