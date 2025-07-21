from django.db import models
from django.utils import timezone
from apis.models.competition import Competition

class DiscountCoupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_affiliate_rc = models.BooleanField(default=False)
    competition = models.ForeignKey(
        Competition, null=True, blank=True, on_delete=models.SET_NULL
    )
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        return self.active and (not self.expires_at or timezone.now() < self.expires_at)

    def __str__(self):
        return f"{self.code} ({self.percentage}%) {'[RC]' if self.is_affiliate_rc else ''}"