from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^canvas_api_token/', include('canvas_api_token.urls')),
)
