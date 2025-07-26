from django.db import models
from apis.models.user_profile import UserProfile
from django.utils import timezone
from apis.models.competition import Competition
from apis.models.winner import Winner


class CompetitionCopyHistory(models.Model):
    original_competition = models.ForeignKey(Competition, related_name='copy_sources', on_delete=models.CASCADE)
    new_competition = models.ForeignKey(Competition, related_name='copied_versions', on_delete=models.CASCADE)
    copied_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    inserted_position = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Copied {self.original_competition.title} → {self.new_competition.title}"

class CompetitionEditLog(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    edited_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    field_changed = models.CharField(max_length=255)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Edit on {self.competition.title} - {self.field_changed}"

class JournalEntry(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    log_type = models.CharField(max_length=100)  # e.g., "entry", "draw", etc.
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)

class LiveDraw(models.Model):
    competitions = models.ManyToManyField(Competition)
    video_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ClientActionLog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=100)
    details = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action_type} at {self.timestamp}"

class TopAllTimeWinner(models.Model):
    winner = models.OneToOneField(Winner, on_delete=models.CASCADE)
    display_order = models.PositiveIntegerField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

class Invoice(models.Model):
    sale = models.OneToOneField('giftshop.Sale', on_delete=models.CASCADE, related_name='invoice')
    order = models.OneToOneField('apis.Order', on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pdf_file = models.FileField(upload_to='invoices/%Y/%m/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Invoice #{self.invoice_number}"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        super().save(*args, **kwargs)

    def generate_invoice_number(self):
        year_suffix = timezone.now().strftime('%y')
        letter = 'A'
        last_invoice = Invoice.objects.filter(invoice_number__startswith=year_suffix + letter).order_by('invoice_number').last()
        if last_invoice:
            last_number = int(last_invoice.invoice_number[-6:])
            next_number = str(last_number + 1).zfill(6)
        else:
            next_number = '000001'
        return f"{year_suffix}{letter}{next_number}"
