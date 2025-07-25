from django.db import models
from apis.models.product_category import ProductCategory

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
    