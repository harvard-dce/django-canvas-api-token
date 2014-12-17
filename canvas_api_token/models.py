from django.db import models

# Create your models here.
class CanvasApiToken(models.Model):
    user_id = models.CharField(max_length=10)
    token = models.CharField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    expires_on = models.DateTimeField(null=True)

    class Meta:
        db_table = u'canvas_api_token'
