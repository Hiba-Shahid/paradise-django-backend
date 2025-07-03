# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    email = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_affiliate = models.BooleanField(default=False)
    is_staff_member = models.BooleanField(default=False)
    rc_code = models.CharField(max_length=20, blank=True, null=True)  
    linked_affiliate = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='leads')
    affiliate_joined_on = models.DateTimeField(null=True, blank=True)
    consent_to_marketing = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username}'s Profile"


class AffiliateProfile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    can_withdraw = models.BooleanField(default=False)
    withdraw_limit_reached = models.BooleanField(default=False)
    last_withdraw_date = models.DateField(null=True, blank=True)

class AffiliateCommission(models.Model):
    affiliate = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    lead = models.ForeignKey(User, related_name='commission_source', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    related_order = models.ForeignKey('Order', on_delete=models.CASCADE)