from django.http import HttpResponseServerError, HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.utils import translation
from django.contrib.auth.decorators import login_required
from urlparse import parse_qs
from github import Github
import requests
from datetime import datetime

from models import Person


# Decorators
def templatable_view(template_name):
    def decorator(view):
        def wrapped_view(request, *a, **kw):
            result = view(request, *a, **kw)
            lang = translation.get_language()

            if not isinstance(result,dict):
                return result

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
    try:
        tmp_name = user_info['name'].split(' ')
        firstname = tmp_name[0]
        lastname = tmp_name[1]
    except:
        firstname = user_info.get('name', None)
        lastname = None

    user, created = User.objects.get_or_create(username=user_info['login'], defaults={
        'username': user_info['login'],
        'backend': 'social_auth.backends.contrib.github.GithubBackend',
        'first_name': firstname,
        'last_name': lastname,
        'email': user_info['email'],
        'is_staff': False,
        'is_active': True,
        'is_superuser': False
    })
    user.backend = 'social_auth.backends.contrib.github.GithubBackend'
    user.save()

    person, created = Person.objects.get_or_create(user=user, defaults={
        'name': user_info['name'],
        'avatar_url': user_info['avatar_url'],
        'github_user_id': user_info['user_id'],
        'company': user_info['company'],
        'location': user_info['location']
    })
    return user, person


def _game_is_started():
    return datetime.now() >= settings.GAME_STARTS_AT

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

@templatable_view('waiting')
def waiting(request):
    print "_game_is_started: %s" % _game_is_started()

    if _game_is_started():
        return HttpResponseRedirect(reverse('home'))

    return {
        "start": settings.GAME_STARTS_AT.strftime('%d/%m/%y %H:%M')
    }

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
                                "login": user.login,
                            }

                            user, person = _create_user(user_info)
                            auth_login(request, user)
                            return HttpResponseRedirect(reverse('kill', kwargs={'user_id': user.id}))
                else:
                    return HttpResponseServerError()

    return HttpResponseBadRequest()


@login_required
@templatable_view('kill')
def kill(request, user_id):

    print "_game_is_started: %s" % _game_is_started()

    if not _game_is_started():
        return HttpResponseRedirect(reverse('waiting'))


    p = Person.objects.get(user__id=user_id)
    username = p.name
    secret_word = p.secret_word
    is_killed = p.is_killed

    error = None
    message = None

    if 'secret_word' in request.POST:
        kill_secret_word = request.POST['secret_word']

        if p.target.secret_word == kill_secret_word:
            p.target.is_killed = True
            p.target.date_killed = datetime.datetime.now()
            p.target.save()

            p.target = p.target.target
            p.save()

            message = "You've just killed your target.  Now kill the next one."
        else:
            error = "That's not the right word.  The kill is not registered."

    return {
        'message': message,
        'error': error,
        'is_killed': is_killed,
        'username': username,
        'target': p.target,
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
