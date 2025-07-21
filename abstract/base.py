from django.db import models


class BaseModel(models.Model):
    id = models.CharField(max_length=15, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["created_at"]


  