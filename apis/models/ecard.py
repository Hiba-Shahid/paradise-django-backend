from django.db import models

class ECard(models.Model):
    code = models.CharField(max_length=10, unique=True)
    video = models.FileField(upload_to='ecards/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_used = models.BooleanField(default=False)  
