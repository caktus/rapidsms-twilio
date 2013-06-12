import datetime

from django.db import models


class TwilioResponse(models.Model):
    date = models.DateTimeField()
    message = models.CharField(max_length=64, primary_key=True)
    account = models.CharField(max_length=64)
    sender = models.CharField(max_length=16)
    recipient = models.CharField(max_length=16)
    status = models.CharField(max_length=16)

    def save(self, **kwargs):
        if not self.date:
            self.date = datetime.datetime.now()
        return super(TwilioResponse, self).save(**kwargs)
