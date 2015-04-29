from functools import wraps
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from models import CanvasApiToken

import logging
log = logging.getLogger(__name__)

def api_token_required(completed_view=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):

            # handle request from existing consumer session
            if 'CANVAS_API_OAUTH_TOKEN' in request.session:
                return view_func(request, *args, **kwargs)

            # handle loading existing token based on username
            try:
                token = CanvasApiToken.objects.get(user=request.user)
                request.session['CANVAS_API_OAUTH_TOKEN'] = token.token
                return view_func(request, *args, **kwargs)
            except CanvasApiToken.DoesNotExist, e:
                pass

            if request.method != 'POST':
                log.error("Invalid request. Token generation can only " \
                    + "happen at lti launch.")
                return HttpResponseBadRequest()

            # get the registered developer key client_id for this consumer and
            # save it so we can look up the client id/secret in the next step
            consumer_key = request.POST.get('oauth_consumer_key', None)
            request.session['OAUTH_CONSUMER_KEY'] = consumer_key

            request.session['CANVAS_API_TOKEN_COMPLETE_REDIRECT_VIEW'] = \
                completed_view or view_func.__name__

            # initiate token generation
            return redirect(reverse('token_init'))

        return _wrapped_view
    return decorator
