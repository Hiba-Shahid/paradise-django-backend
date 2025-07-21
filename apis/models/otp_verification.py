from django.db import models
from abstract.base import BaseModel
from abstract.timestamp import TimeStamp
from apis.models.user_profile import UserProfile 

class OTPVerification(BaseModel, TimeStamp):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='otp_codes')
    code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    purpose = models.CharField(max_length=50, default='registration')

    def __str__(self):
        return f"OTP for {self.user_profile.user.username} - {self.code} ({'Verified' if self.is_verified else 'Pending'})"
