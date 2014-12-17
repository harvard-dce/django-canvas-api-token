from urlparse import urlparse, parse_qs
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.test import TestCase
from mock import MagicMock, patch
from canvas_api_token.decorators import api_token_required
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from functools import WRAPPER_ASSIGNMENTS
from canvas_api_token import models, views
from django.http import HttpResponseBadRequest

class BaseTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='foo', email='foo@example.edu', password='bar'
        )

    def _fake_request(self, path='/', method='GET', params={}):
        if method == 'POST':
            request = self.factory.post(path, params)
        else:
            request = self.factory.get(path, params)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = self.user
        return request

    def _decorated_view(self, mock_view, **decorator_kwargs):
        for attr in WRAPPER_ASSIGNMENTS:
            setattr(mock_view, attr, 'fake_view_func' + attr)
        return api_token_required(**decorator_kwargs)(mock_view)


class DecoratorTests(BaseTestCase):

    def test_token_in_session(self):
        mock_view = MagicMock()
        decorated_view = self._decorated_view(mock_view)
        request = self._fake_request()
        request.session['CANVAS_API_OAUTH_TOKEN'] = 'hola!'
        response = decorated_view(request)
        self.assertTrue(mock_view.called)

    def test_token_in_db(self):
        mock_view = MagicMock()
        decorated_view = self._decorated_view(mock_view)
        request = self._fake_request()
        token = models.CanvasApiToken(user_id=request.user.username, token='abc123')
        token.save()
        response = decorated_view(request)
        self.assertTrue(mock_view.called)
        self.assertTrue(request.session['CANVAS_API_OAUTH_TOKEN'] == 'abc123')

    def test_no_token_using_GET(self):
        mock_view = MagicMock()
        decorated_view = self._decorated_view(mock_view)
        request = self._fake_request()
        response = decorated_view(request)
        self.assertTrue(isinstance(response, HttpResponseBadRequest))

    def test_no_token_using_POST(self):
        mock_view = MagicMock()
        decorated_view = self._decorated_view(mock_view)
        request = self._fake_request(method='POST')
        response = decorated_view(request)
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.url, '/canvas_api_token/token_init')

    def test_no_token_lti_launch(self):
        mock_view = MagicMock()
        decorated_view = self._decorated_view(mock_view)
        request = self._fake_request(method='POST', params={'oauth_consumer_key': 'asdf1234'})
        response = decorated_view(request)
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.url, '/canvas_api_token/token_init')
        self.assertEqual(request.session['OAUTH_CONSUMER_KEY'], 'asdf1234')

    def test_redirect_view_arg(self):
        mock_view = MagicMock()
        decorated_view = self._decorated_view(mock_view, completed_view='baz')
        request = self._fake_request(method='POST')
        response = decorated_view(request)
        self.assertEqual(request.session['CANVAS_API_TOKEN_COMPLETE_REDIRECT_VIEW'], 'baz')


class ViewTests(BaseTestCase):

    # override creation of initial 'state' value
    @patch('canvas_api_token.views.uuid4', MagicMock(return_value='my-random-string'))
    def test_token_init(self):

        request = self._fake_request()
        request.session['OAUTH_CONSUMER_KEY'] = 'test_consumer'
        request.session['LTI_LAUNCH'] = {'launch_presentation_return_url': 'http://example.edu:1234'}

        response = views.token_init(request)

        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertTrue(response.url.startswith('http://example.edu:1234'))
        url_parts = urlparse(response.url)
        query = parse_qs(url_parts.query)
        self.assertEqual(query['state'], ['my-random-string'])
        pass

    @patch('canvas_api_token.views.uuid4', MagicMock(return_value='my-random-string'))
    @patch('canvas_api_token.views.token_request', MagicMock(return_value='my-token'))
    def test_token_retrieve(self):

        request = self._fake_request(params={'code': '98765', 'state': 'my-random-string'})
        request.session['CANVAS_API_OAUTH_INITIAL_STATE'] = 'my-random-string'
        request.session['OAUTH_CONSUMER_KEY'] = 'test_consumer'
        request.session['LTI_LAUNCH'] = {'launch_presentation_return_url': 'http://example.edu:1234'}
        # just re-use existing url pattern so we don't have to bother setting
        # up a full test view/url/etc
        request.session['CANVAS_API_TOKEN_COMPLETE_REDIRECT_VIEW'] = 'token_retrieve'
        response = views.token_retrieve(request)
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(request.session['CANVAS_API_OAUTH_TOKEN'], 'my-token')

    def test_token_retrieve_error(self):

        request = self._fake_request(params={'error': 'an error occurred!'})
        response = views.token_retrieve(request)
        self.assertTrue(isinstance(response, HttpResponseServerError))

    def test_token_retrieve_state_mismatch(self):

        request = self._fake_request(params={'code': 'foo', 'state': 'not-the-right-state'})
        request.session['CANVAS_API_OAUTH_INITIAL_STATE'] = 'the-right-state'
        response = views.token_retrieve(request)
        self.assertTrue(isinstance(response, HttpResponseBadRequest))



