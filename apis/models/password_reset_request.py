from django.db import models
from user_profile import UserProfile


class PasswordResetRequest(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()