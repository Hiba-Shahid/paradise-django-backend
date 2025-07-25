from django.db import models
from apis.models.user_profile import UserProfile  


class Newsletter(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True)

class NewsletterSubscription(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

class AutoReply(models.Model):
    trigger = models.CharField(max_length=50)
    subject = models.CharField(max_length=255)
    body = models.TextField()

class CustomerMessage(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)