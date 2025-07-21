from django.db import models
from datetime import timedelta
from django.utils import timezone
from apis.models.competition_category import CompetitionCategory



class Competition(models.Model):
    STATUS_CHOICES = [('prepared', 'Prepared'), ('active', 'Active'), ('past', 'Past')]
    category = models.ForeignKey(CompetitionCategory, on_delete=models.CASCADE, related_name='competitions')
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_description = models.CharField(max_length=55, null=True, blank=True)
    live_draw_date = models.DateTimeField()
    closing_date = models.DateTimeField()
    extension_count = models.PositiveIntegerField(default=0)
    number_of_winners = models.PositiveIntegerField(default=30)
    ticket_letter_limit = models.PositiveSmallIntegerField(default=1)
    tickets_per_letter = models.PositiveIntegerField(default=100) 
    ticket_purchase_limit_per_user = models.PositiveIntegerField(default=7)
    is_coupon_competition = models.BooleanField(default=False)

    class Meta:
        ordering = ['-live_draw_date']

    def save(self, *args, **kwargs):
        if not self.code:
            today_str = timezone.now().strftime("%y%m%d")
            base_code = f"{today_str}"
            counter = 1
            while True:
                generated_code = f"{base_code}{str(counter).zfill(2)}"
                if not Competition.objects.filter(code=generated_code).exists():
                    self.code = generated_code
                    break
                counter += 1
        super().save(*args, **kwargs)

    def extend_closing_date(self):
        if self.extension_count < self.max_extensions_allowed:
            self.closing_date += timedelta(days=7)
            self.extension_count += 1
            self.save()

    def __str__(self):
        return self.title

    @property
    def total_past_winners(self):
        from apis.models.winner import Winner
        return Winner.objects.filter(ticket__competition=self).count()

    @property
    def total_prize_value(self):
        from apis.models.winner import Winner
        return sum([
            winner.instant_prize.giveaway_count if winner.is_instant_win and winner.instant_prize else 0
            for winner in Winner.objects.filter(ticket__competition=self)
        ])

    @property
    def total_tickets(self):
        return (26 ** self.ticket_letter_limit) * self.tickets_per_letter