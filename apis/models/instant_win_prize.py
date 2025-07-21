from django.db import models
from apis.models.competition import Competition


class InstantWinPrize(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    prize_title = models.CharField(max_length=255)
    prize_description = models.TextField()
    giveaway_count = models.PositiveIntegerField()
    image = models.ImageField(upload_to='instant_wins/', null=True, blank=True)
    won_at = models.DateTimeField(auto_now_add=True)