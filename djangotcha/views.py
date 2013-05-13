from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.conf import settings
from django.utils import translation
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from urlparse import urlparse, parse_qs
from github import Github
import requests
import json
import datetime

from models import Person

# Decorators
def templatable_view(template_name):
    def decorator(view):
        def wrapped_view(request, *a, **kw):
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


def _create_user(user_info):
    p = Person(
        name=user_info['name'],
        avatar_url=user_info['avatar_url'],
        github_user_id=user_info['user_id']
    )
    p.save()


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

    if 'redirect_state' in request.REQUEST and 'state' in request.REQUEST:
        if request.REQUEST['redirect_state'] == request.REQUEST['state']:

            if 'code' in request.REQUEST:
                code = request.REQUEST['code']

                # fetch an access_token
                post_data = {
                    "code": code,
                    "client_id": settings.GITHUB_APP_ID,
                    "client_secret": settings.GITHUB_API_SECRET,
                }
                r = requests.post(settings.GITHUB_REQUEST_TOKEN_URL, data=post_data)

                if r.status_code == 200:
                    github_response = parse_qs(r.content)
                    print github_response

                    if 'error' in github_response:
                        return HttpResponseServerError(github_response['error'][0])
                    else:
                        if 'access_token' in github_response:
                            access_token = github_response['access_token'][0]

                            github = Github(access_token)
                            user = github.get_user()

                            #see: https://github.com/jacquev6/PyGithub/blob/master/github/AuthenticatedUser.py
                            user_info = {
                                "avatar_url": user.avatar_url,
                                "company": user.company,
                                "email": user.email,
                                "user_id": user.id,
                                "location": user.location,
                                "name": user.name,
                            }

                            print user_info

                            _create_user(user_info)

                            return user_info

                else:
                    return HttpResponseServerError()

    return HttpResponseBadRequest()

@templatable_view('kill')
def kill(request, user_id):

    p = Person.objects.get(id=user_id)
    username = p.name
    target = p.target
    secret_word = p.secret_word
    is_killed = p.is_killed

    error = None

    if 'secret_word' in request.POST:
        kill_secret_word = request.POST['secret_word']

        import pdb
        pdb.set_trace()

        if target.secret_word == kill_secret_word:
            target.is_killed = True
            target.date_killed = datetime.datetime.now()
            target.save()

            p.target = target.target
            p.save()
        else:
            error = "secret_word not correct"


    return {
        'error': error,
        'is_killed': is_killed,
        'username': username,
        'target': target,
        'secret_word': secret_word,
        'user_id': user_id,
    }

@templatable_view('home')
def rules(request):
    return {}

@templatable_view('404')
def error404(request):
    return {}

@templatable_view('500')
def error500(request):
    raise Exception('Dummy internal server error')
