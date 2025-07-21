from django.db import models
from apis.models.competition import Competition
from apis.models.user_profile import UserProfile
from apis.models.ecard import ECard


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold'),
    ]

    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="tickets")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    ticket_number = models.CharField(max_length=10)
    ecard = models.ForeignKey(ECard, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    
    class Meta:
        unique_together = ( 'competition', 'ticket_number')

    def __str__(self):
        return f"{self.ticket_number} - {self.status}"