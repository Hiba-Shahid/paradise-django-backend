from django.db import models
from affiliate_profile import AffiliateProfile

class AffiliateWithdrawal(models.Model):
    affiliate = models.ForeignKey(AffiliateProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='pending')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.affiliate.user.user.username} withdrawal - {self.amount} ({self.status})"
