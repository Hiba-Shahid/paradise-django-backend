from django.db import models
from django.contrib.auth.models import User
from abstract.base import BaseModel


class UserProfile(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone = models.CharField(max_length=20, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True) 
    updated_at = models.DateTimeField(auto_now=True)
    is_allow_affiliate_marketing = models.BooleanField(default=False)
    referrar = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='referees')


    def __str__(self):
        return f"{self.user.username}'s Profile"