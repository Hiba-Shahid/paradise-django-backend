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

    def __str__(self):
        return self.title

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
    ticket_letter_limit = models.PositiveSmallIntegerField(default=26)  
    ticket_number_limit = models.PositiveSmallIntegerField(default=1000)  
    ticket_purchase_limit_per_user = models.PositiveIntegerField(default=7)
    is_coupon_competition = models.BooleanField(default=False)
    is_discounted_now = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_discounted = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['-live_draw_date']

    def save(self, *args, **kwargs):
        if not self.unique_code:
            today_str = timezone.now().strftime("%y%m%d")
            self.unique_code = f"{today_str}01"
        self.sold_out = self.entries_left == 0
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
        from .models import Winner  
        return Winner.objects.filter(ticket__competition=self).count()

    @property
    def total_prize_value(self):
        from .models import Winner
        return sum([winner.prize.value for winner in Winner.objects.filter(ticket__competition=self)])
    
class CompetitionPrize(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='prizes')
    prize_position = models.PositiveSmallIntegerField()  
    ticket_number = models.CharField(max_length=10)
    prize_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.competition.title} - {self.prize_position} Prize"
    
    @classmethod
    def get_all_time_prize_value(cls):
        return sum(cls.objects.values_list('prize_value', flat=True))


class DiscountCoupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_affiliate_rc = models.BooleanField(default=False)
    competition_group = models.ForeignKey(
        CompetitionGroup, null=True, blank=True, on_delete=models.SET_NULL
    )
    active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        return self.active and (not self.expires_at or timezone.now() < self.expires_at)

    def __str__(self):
        return f"{self.code} ({self.percentage}%) {'[RC]' if self.is_affiliate_rc else ''}"


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

class TicketRange(models.Model):
        RANGE_CHOICES = [
            ('A-A', 'A-A'), ('A-Z', 'A-Z'),
            ('100', '100'), ('200', '200'), ('300', '300'),
            ('400', '400'), ('500', '500'), ('600', '600'),
            ('700', '700'), ('800', '800'), ('900', '900'), ('1000', '1000'),
        ]
        competition = models.OneToOneField(Competition, on_delete=models.CASCADE)
        range_type = models.CharField(max_length=10, choices=RANGE_CHOICES)
    
        def __str__(self):
            return f"{self.competition.title} - Range {self.range_type}"


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
