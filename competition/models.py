from main.models import UserProfile
from django.db import models

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


    def __str__(self):
        return self.title

    def tickets_sold(self):
        return self.total_tickets - self.remaining_tickets

class ECard(models.Model):
    code = models.CharField(max_length=10, unique=True)
    video = models.FileField(upload_to='ecards/')
    is_active = models.BooleanField(default=True)

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
    

class Winner(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='wins')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='winners')
    prize = models.CharField(max_length=255)
    win_date = models.DateTimeField(auto_now_add=True)
    prize_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ], default='pending')

    def __str__(self):
        return f"{self.user.username} won {self.prize} in {self.competition.name}"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('card', 'Card'),
        ('wallet', 'Wallet'),
        ('site_credit', 'Site Credit'),
        ('paypal', 'PayPal'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    competition = models.ForeignKey(
        Competition, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='payments'
    )
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user.username} - {self.amount} via {self.payment_method}"
    
class JournalEntry(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
