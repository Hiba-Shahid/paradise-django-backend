from django.db import models
from abstract.base import BaseModel
from abstract.timestamp import TimeStamp
from apis.models.user_profile import UserProfile


class PasswordResetRequest(BaseModel, TimeStamp):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    is_used = models.BooleanField(default=False)
  