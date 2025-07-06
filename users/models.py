# Create your models here.
import uuid
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
    rc_code = models.CharField(max_length=20, blank=True, null=True,  unique=True)  
    linked_affiliate = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='leads')
    affiliate_joined_on = models.DateTimeField(null=True, blank=True)
    consent_to_marketing = models.BooleanField(default=False)
    receive_whatsapp = models.BooleanField(default=False)
    receive_email = models.BooleanField(default=True)
    marketing_consent = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_affiliate and not self.rc_code:
            self.rc_code = str(uuid.uuid4()).split('-')[0].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class AffiliateProfile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='affiliate')
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_withdraw_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Affiliate: {self.user.user.username}"

    def can_withdraw(self):
        return self.user.leads.count() >= 5 and self.total_earnings >= 25.0


class AffiliateWithdrawal(models.Model):
    affiliate = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
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
        return f"{self.affiliate.user.username} withdrawal - {self.amount} ({self.status})"


class AffiliateCommission(models.Model):
    affiliate = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    lead = models.ForeignKey(UserProfile, related_name='commission_source', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    related_order = models.ForeignKey('Order', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.affiliate.user.username} earned {self.amount} from {self.lead.user.username}"


class Wallet(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return f"{self.user_profile.user.username}'s Wallet - Balance: {self.balance}"


class WalletTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
        ('withdrawal', 'Withdrawal'),
        ('commission', 'Commission'),
        ('reward', 'Reward'),
    ]
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    related_order = models.ForeignKey('giftshop.Order', null=True, blank=True, on_delete=models.SET_NULL)

class OTPVerification(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='otp_verifications')
    code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    purpose = models.CharField(max_length=50, default='registration') 

class NewsletterSubscription(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)


class LoginHistory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class PasswordResetRequest(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()


class ClientActionLog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=100)  
    details = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action_type} at {self.timestamp}"
