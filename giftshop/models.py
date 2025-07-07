from django.db import models
from users.models import UserProfile
from django.utils.timezone import now
from competition.models import Competition, Ticket

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [('digital', 'Digital'), ('physical', 'Physical')]

    name = models.CharField(max_length=255)
    description = models.TextField()
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES)
    file = models.FileField(upload_to='giftshop/', null=True, blank=True)
    image = models.ImageField(upload_to='giftshop/images/')
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL)
    is_featured_homepage = models.BooleanField(default=False)
    is_general_ecard = models.BooleanField(default=False)
    competition_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def is_digital(self):
        return self.product_type == 'digital'

    @property
    def is_out_of_stock(self):
        return self.product_type == 'physical' and self.stock == 0
    

class Cart(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user_profile}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    ticket = models.ForeignKey(Ticket, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    
    def __str__(self):
        return f"Item in {self.cart}"


class Order(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    competition = models.ForeignKey(Competition, null=True, blank=True, on_delete=models.SET_NULL)
    rc_code_used = models.CharField(max_length=20, null=True, blank=True)
    unique_sale_code = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.unique_sale_code} by {self.user_profile}"
    
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    ticket = models.ForeignKey(Ticket, null=True, blank=True, on_delete=models.SET_NULL)
    competition = models.ForeignKey(Competition, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    sale_code = models.CharField(max_length=50, unique=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    
def save(self, *args, **kwargs):
    if not self.sale_code:
        date_part = now().strftime('%y%m%d')
        base_code = f"{date_part}01A"
        existing = Sale.objects.filter(sale_code__startswith=base_code).count()
        next_num = str(existing + 1).zfill(3)
        self.sale_code = f"{base_code}{next_num}"
    super().save(*args, **kwargs)

    def __str__(self):
        return self.sale_code


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    ticket = models.ForeignKey(Ticket, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Item in Order #{self.order.unique_sale_code}"

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

    def __str__(self):
        return f"Transaction {self.gateway_reference} for Order #{self.order.unique_sale_code}"


