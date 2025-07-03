from django.db import models
from users.models import UserProfile
from competition.models import Competition, Ticket

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_digital = models.BooleanField(default=False)
    file = models.FileField(upload_to='giftshop/', null=True, blank=True)
    image = models.ImageField(upload_to='giftshop/images/')
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL)

class Cart(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    competition = models.ForeignKey(Competition, null=True, blank=True, on_delete=models.SET_NULL)
    ticket_quantity = models.PositiveIntegerField(default=1)
    quantity = models.PositiveIntegerField(default=1) 

    def is_ticket(self):
        return self.competition is not None

    def __str__(self):
        if self.product:
            return f"{self.quantity} x {self.product.name}"
        elif self.competition:
            return f"{self.ticket_quantity} ticket(s) for {self.competition.title}"
        return "Invalid cart item"


class Order(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    competition = models.ForeignKey(Competition, null=True, blank=True, on_delete=models.SET_NULL)
    rc_code_used = models.CharField(max_length=20, null=True, blank=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    ticket = models.ForeignKey(Ticket, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=8, decimal_places=2)

class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    gateway_reference = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    paid_at = models.DateTimeField()
    raw_response = models.JSONField()
    payment_method = models.CharField(max_length=50)
    retried = models.BooleanField(default=False)
    is_refunded = models.BooleanField(default=False)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    retry_attempts = models.PositiveIntegerField(default=0)


class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=20, unique=True)
    pdf_file = models.FileField(upload_to='invoices/')
    created_at = models.DateTimeField(auto_now_add=True)



