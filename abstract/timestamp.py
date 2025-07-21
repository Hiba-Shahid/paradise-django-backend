from django.db import models


class TimeStamp(models.Model):
    expires_at = models.DateTimeField()

    class Meta:
        abstract = True