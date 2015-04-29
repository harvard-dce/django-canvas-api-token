import requests
from uuid import uuid4
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.decorators.http import require_GET
from django.http import HttpResponseServerError, HttpResponseBadRequest
from models import CanvasApiToken
from utils import absolute_uri, canvas_uri, get_client_credentials

@login_required
@require_GET
def token_init(request):

    # generate & store a random 'state' value that can be validated in the next step
    state = str(uuid4())
    request.session['CANVAS_API_OAUTH_INITIAL_STATE'] = state

    redirect_uri = absolute_uri(request, 'token_retrieve')
    client_cred = get_client_credentials(request)

    # params to generate the user's api token
    token_gen_params = {
        'client_id': client_cred['client_id'],
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'state': state,
    }

    # redirect to canvas to initiate the token creation
    token_gen_uri = canvas_uri(request, '/login/oauth2/auth', token_gen_params)
    return redirect(token_gen_uri)

@login_required
@require_GET
def token_retrieve(request):

    if 'error' in request.GET:
        return HttpResponseServerError(
            'Failed to create Canvas API oauth token: ' \
             + request.GET['error'])

    oauth_code = request.GET.get('code')
    oauth_state = request.GET.get('state')

    if oauth_state != request.session['CANVAS_API_OAUTH_INITIAL_STATE']:
        return HttpResponseBadRequest("Oauth state mismatch")

    client_cred = get_client_credentials(request)

    # this needs to be the same url as in the token_init view because
    # canvas uses it for validation purposes; not actually used for redirection
    redirect_uri = absolute_uri(request, 'token_retrieve')

    token_retrieve_params = {
        'client_id': client_cred['client_id'],
        'client_secret': client_cred['client_secret'],
        'code': oauth_code,
        'redirect_uri': redirect_uri,
    }

    token_retrieve_uri = canvas_uri(request, '/login/oauth2/token')

    try:
        token = token_request(token_retrieve_uri, token_retrieve_params)
    except Exception, e:
        return HttpResponseServerError("Failed to fetch generate token: " \
            + str(e))

    user_token = CanvasApiToken(user=request.user, token=token)
    user_token.save()
    request.session['CANVAS_API_OAUTH_TOKEN'] = token

    final_uri = reverse(request.session['CANVAS_API_TOKEN_COMPLETE_REDIRECT_VIEW'])
    return redirect(final_uri)

def token_request(uri, post_params):
    """
    This method should be overwritten by django project code that wishes to
    handle http sub-requests differently, eg, async requests
    :param uri: uri to fetch
    :param post_params: post parameter dictionary
    :return: formatted string
    """
    r = requests.post(uri, post_params)
    r.raise_for_status()
    response_data = r.json()
    return response_data['access_token']
