from django.db import models
from user_profile import UserProfile

class OTPVerification(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='otp_verifications')
    code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    purpose = models.CharField(max_length=50, default='registration') 