from main.models import UserProfile
from django.db import models

class Competition(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('upcoming', 'Upcoming'),
        ('ended', 'Ended'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    prize_name = models.CharField(max_length=255)
    prize_images = models.JSONField(default=list)  
    price_per_entry = models.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = models.PositiveIntegerField()
    remaining_tickets = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def tickets_sold(self):
        return self.total_tickets - self.remaining_tickets


class Ticket(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tickets')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='tickets')
    ticket_number = models.CharField(max_length=50, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket #{self.ticket_number} - {self.user.username}"
    

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