from django.conf.urls import patterns, url

urlpatterns = patterns('canvas_api_token.views',
    url(r'^token_init$', 'token_init', name='token_init'),
    url(r'^token_retrieve$', 'token_retrieve', name='token_retrieve'),
)
