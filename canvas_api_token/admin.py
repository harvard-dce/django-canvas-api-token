
from django.contrib import admin
from canvas_api_token.models import CanvasApiToken, CanvasDeveloperKey

admin.site.register(CanvasApiToken)
admin.site.register(CanvasDeveloperKey)
