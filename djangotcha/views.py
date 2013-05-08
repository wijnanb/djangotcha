from django.http import HttpResponseNotFound
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.conf import settings
from django.utils import translation
from django.core.mail import send_mail

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
            if 'user' in request.session:
                context['user_data'] = request.session['user']

            context.update(result)

            template = template_name + '.html'
            return render_to_response(template, context, context_instance=RequestContext(request))
        return wrapped_view
    return decorator

# Views
@templatable_view('home')
def home(request):
    return {}

@templatable_view('authorized')
def authorized(request):
    return {}

def signin(request):
    import oauth2

    import urlparse
    import oauth2 as oauth

    oauth_settings = settings.GITHUB_APP

    consumer_key = oauth_settings['client_id']
    consumer_secret = oauth_settings['client_secret']

    request_token_url = oauth_settings['request_token_url']
    access_token_url = oauth_settings['access_token_url']
    authorize_url = oauth_settings['authorize_url']

    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)

    # Step 1: Get a request token. This is a temporary token that is used for
    # having the user authorize an access token and to sign the request to obtain
    # said access token.

    resp, content = client.request(request_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])

    request_token = dict(urlparse.parse_qsl(content))

    print "Request Token:"
    print "    - oauth_token        = %s" % request_token['oauth_token']
    print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']
    print

    # Step 2: Redirect to the provider. Since this is a CLI script we do not
    # redirect. In a web application you would redirect the user to the URL
    # below.

    print "Go to the following link in your browser:"
    print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
    print

    # After the user has granted access to you, the consumer, the provider will
    # redirect you to whatever URL you have told them to redirect to. You can
    # usually define this in the oauth_callback argument as well.
    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = raw_input('Have you authorized me? (y/n) ')
    oauth_verifier = raw_input('What is the PIN? ')

    # Step 3: Once the consumer has redirected the user back to the oauth_callback
    # URL you can request the access token the user has approved. You use the
    # request token to sign this request. After this is done you throw away the
    # request token and use the access token returned. You should store this
    # access token somewhere safe, like a database, for future use.
    token = oauth.Token(request_token['oauth_token'],
        request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))

    print "Access Token:"
    print "    - oauth_token        = %s" % access_token['oauth_token']
    print "    - oauth_token_secret = %s" % access_token['oauth_token_secret']
    print
    print "You may now access protected resources using the access tokens above."
    print




@templatable_view('404')
def error404(request):
    return {}

@templatable_view('500')
def error500(request):
    raise Exception('Dummy internal server error')
