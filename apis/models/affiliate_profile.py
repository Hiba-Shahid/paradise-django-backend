import uuid
from django.db import models
from user_profile import UserProfile


class AffiliateProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='affiliate')
    rc_code = models.CharField(max_length=20, unique=True, null=True, blank=True)  
    affiliate_joined_on = models.DateTimeField(null=True, blank=True)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
       if not self.rc_code:
          self.rc_code = str(uuid.uuid4()).split('-')[0].upper()
       super().save(*args, **kwargs)


    def __str__(self):
        return f"Affiliate: {self.user.user.username}"

    def can_withdraw(self):
        return self.user.leads.count() >= 5 and self.total_earnings >= 25.0
