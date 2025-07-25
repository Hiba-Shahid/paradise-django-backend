from django.db import models
from apis.models.user_profile import UserProfile
from django.utils.timezone import now
from apis.models.competition import Competition
from apis.models.ticket import Ticket
from apis.models.product import Product
from apis.models.order import Order

    
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    ticket = models.ForeignKey(Ticket, null=True, blank=True, on_delete=models.SET_NULL)
    competition = models.ForeignKey(Competition, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    sale_code = models.CharField(max_length=50, unique=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.sale_code:
            date_part = now().strftime('%y%m%d')
            base_code = f"{date_part}01A"
            existing = Sale.objects.filter(sale_code__startswith=base_code).count()
            next_num = str(existing + 1).zfill(3)
            self.sale_code = f"{base_code}{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.sale_code


class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    gateway_reference = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    paid_at = models.DateTimeField()
    raw_response = models.JSONField()
    payment_method = models.CharField(max_length=50)
    retried = models.BooleanField(default=False)
    is_refunded = models.BooleanField(default=False)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    retry_attempts = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Transaction {self.gateway_reference} for Order #{self.order.unique_sale_code}"


