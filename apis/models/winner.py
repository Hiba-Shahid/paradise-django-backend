from django.db import models
from apis.models.ticket import Ticket
from apis.models.competition import Competition
from apis.models.instant_win_prize import InstantWinPrize
from abstract.base import BaseModel

class Winner(BaseModel):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    prize = models.ForeignKey(Competition, on_delete=models.CASCADE)
    instant_prize = models.ForeignKey(InstantWinPrize, null=True, blank=True, on_delete=models.SET_NULL)
    is_instant_win = models.BooleanField(default=False)
    winner_picture = models.ImageField(upload_to='winners/', null=True, blank=True)
    winner_video = models.FileField(upload_to='winners/', null=True, blank=True)
    

    def __str__(self):
        return f"Winner: {self.ticket.ticket_number} | Instant: {self.is_instant_win}"