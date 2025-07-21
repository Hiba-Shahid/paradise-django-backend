from django.db import models
from abstract.base import BaseModel
from apis.models.affiliate_profile import AffiliateProfile
from apis.models.affiliate_withdrawal import AffiliateWithdrawal

class AffiliateTransaction(BaseModel):
    referrar = models.ForeignKey(AffiliateProfile, on_delete=models.CASCADE)
    withdrawal_request = models.OneToOneField(AffiliateWithdrawal, null=True,blank=True, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    TRANSACTION_TYPES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    related_order = models.ForeignKey('giftshop.Order', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
         return f"{self.referrar.user.username} | {self.transaction_type.upper()} of {self.value} | Balance: {self.balance_after}"
