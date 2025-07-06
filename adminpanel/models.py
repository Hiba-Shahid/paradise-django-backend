from django.db import models
from users.models import UserProfile
# Create your models here.

class StaffMember(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    can_delete = models.BooleanField(default=False)
    can_publish = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
