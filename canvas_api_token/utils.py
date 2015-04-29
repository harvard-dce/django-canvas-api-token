import urllib
from django.core.exceptions import SuspiciousOperation, ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.conf import settings
from urlparse import urlparse, urlunparse
from models import CanvasDeveloperKey

import logging
log = logging.getLogger(__name__)

def absolute_uri(request, url_pattern):
    path = reverse(url_pattern)
    return request.build_absolute_uri(path)

def canvas_uri(request, path="", params={}):
    """
    Assembles a uri for the canvas tool consumer instance.
    Assumes presence of 'LTI_LAUNCH' params in the session
    :param request: the django request obj
    :param path: uri path element
    :param params: dict of query params
    :return: uri string
    """
    try:
        launch_params = request.session['LTI_LAUNCH']
        launch_pres_return_url = launch_params['launch_presentation_return_url']
    except KeyError, e:
        msg = "LTI_LAUNCH params missing from request.session: " + str(e)
        log.error(msg)
        raise SuspiciousOperation(msg)
    params = urllib.urlencode(params)
    url_parts = urlparse(launch_pres_return_url)
    return urlunparse([
        url_parts.scheme,
        url_parts.netloc,
        path,
        "",
        params,
        ""
    ])

def get_client_credentials(request):
    """
    retrieves the canvas developer key credentials from your settings
    :param request: HttpRequest
    :return: dict containing client id & secret
    """
    try:
        consumer_key = request.session['OAUTH_CONSUMER_KEY']
        dev_key = CanvasDeveloperKey.objects.get(consumer_key=consumer_key)
        return {
            'client_id': dev_key.client_id,
            'client_secret': dev_key.client_secret
        }
    except CanvasDeveloperKey.DoesNotExist:
        msg = "Can't find developer key entry for {}".format(consumer_key)
        log.error(msg)
        raise ImproperlyConfigured(msg)

