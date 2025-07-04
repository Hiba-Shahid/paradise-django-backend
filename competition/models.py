from users.models import UserProfile
from django.db import models
from datetime import timedelta
from django.utils import timezone

class Prize(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=[('HER', 'HER'), ('HIM', 'HIM'), ('HOME', 'HOME'), ('KIDS', 'KIDS'), ('TECH', 'TECH')])
    media = models.JSONField(default=list) 

class CompetitionGroup(models.Model):
    title = models.CharField(max_length=255)
    is_coupon_competition = models.BooleanField(default=False)

class Competition(models.Model):
    STATUS_CHOICES = [('prepared', 'Prepared'), ('active', 'Active'), ('past', 'Past')]

    unique_code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    group = models.ForeignKey(CompetitionGroup, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    first_day_price = models.DecimalField(max_digits=8, decimal_places=2)
    published_price = models.DecimalField(max_digits=8, decimal_places=2)
    max_entries = models.PositiveIntegerField()
    entries_left = models.PositiveIntegerField()
    live_draw_date = models.DateTimeField()
    closing_date = models.DateTimeField()
    extension_count = models.PositiveIntegerField(default=0)
    sold_out = models.BooleanField(default=False)
    discount_active = models.BooleanField(default=False)
    live_draw_completed = models.BooleanField(default=False)
    number_of_winners = models.PositiveIntegerField(default=1)
    show_winner_summary = models.BooleanField(default=False)  
    promo_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    trustpilot_link = models.URLField(null=True, blank=True)
    facebook_like_link = models.URLField(null=True, blank=True)
    facebook_community_link = models.URLField(null=True, blank=True)
    max_extensions_allowed = models.PositiveIntegerField(default=4)
    promo_video_url = models.URLField(null=True, blank=True)
    promo_image = models.ImageField(upload_to='competitions/promos/', null=True, blank=True)
    ticket_letter_limit = models.PositiveSmallIntegerField(default=26)  # 1-26 (A-Z)
    ticket_number_limit = models.PositiveSmallIntegerField(default=1000)  # 100, 200,...1000
    ticket_purchase_limit_per_user = models.PositiveIntegerField(default=7)


    def extend_closing_date(self):
        if self.extension_count < self.max_extensions_allowed:
            self.closing_date += timedelta(days=7)
            self.extension_count += 1
            self.save()

    def __str__(self):
        return self.title

    def tickets_sold(self):
        return self.max_entries - self.entries_left

    @property
    def total_past_winners(self):
        from .models import Winner  
        return Winner.objects.filter(ticket__competition=self).count()

    @property
    def total_prize_value(self):
        from .models import Winner
        return sum([winner.prize.value for winner in Winner.objects.filter(ticket__competition=self)])

class CouponCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    competition_group = models.ForeignKey(CompetitionGroup, on_delete=models.CASCADE)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        now = timezone.now()
        return self.active and (self.expires_at is None or self.expires_at > now)

    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%"


class ECard(models.Model):
    code = models.CharField(max_length=10, unique=True)
    video = models.FileField(upload_to='ecards/')
    is_active = models.BooleanField(default=True)
    is_used = models.BooleanField(default=False)  



class TicketLock(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    letter = models.CharField(max_length=1)  # A-Z
    number = models.PositiveIntegerField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    locked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('competition', 'letter', 'number')

    def is_expired(self):
        return timezone.now() > self.locked_at + timedelta(minutes=10)


class Ticket(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=10)
    ecard = models.ForeignKey(ECard, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_winner = models.BooleanField(default=False)
    win_rank = models.PositiveSmallIntegerField(null=True, blank=True)  
    attributed_manually = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('competition', 'ticket_number')

class InstantWinPrize(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    prize_title = models.CharField(max_length=255)
    prize_description = models.TextField()
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='instant_wins/', null=True, blank=True)

class TicketInstantWin(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    instant_win_prize = models.ForeignKey(InstantWinPrize, on_delete=models.CASCADE)
    won_at = models.DateTimeField(auto_now_add=True)

    

class Winner(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    winner_picture = models.ImageField(upload_to='winners/', null=True, blank=True)
    winner_video = models.FileField(upload_to='winners/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class TopAllTimeWinner(models.Model):
    winner = models.OneToOneField(Winner, on_delete=models.CASCADE)
    display_order = models.PositiveIntegerField(unique=True)  
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    
class JournalEntry(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)

class LiveDraw(models.Model):
    competitions = models.ManyToManyField(Competition)
    video_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
