from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class CanvasApiToken(models.Model):
    user = models.ForeignKey(User, null=True)
    token = models.CharField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    expires_on = models.DateTimeField(null=True)

    def __str__(self):
        return "Api Token for {}".format(self.user_id)

    class Meta:
        db_table = u'canvas_api_token'

class CanvasDeveloperKey(models.Model):
    consumer_key = models.CharField(max_length=30, unique=True)
    client_id = models.CharField(max_length=30)
    client_secret = models.CharField(max_length=100)

    def __str__(self):
        return "Developer Key {} for {}".format(
            self.client_id, self.consumer_key)

    class Meta:
        db_table = u'canvas_dev_key'
