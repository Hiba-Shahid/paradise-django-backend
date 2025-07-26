from django.db import models
from apis.models.user_profile import UserProfile
import uuid

class Order(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    rc_code_used = models.CharField(max_length=20, null=True, blank=True)
    sale_code = models.CharField(max_length=20, unique=True, blank=True, editable=False)


    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.sale_code} by {self.user_profile}"
    
    def save(self, *args, **kwargs):
        if not self.sale_code:
            self.sale_code = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args,**kwargs)
    