from django.db import models
from apis.models.cart import Cart
from apis.models.product import Product
from apis.models.ticket import Ticket

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    ticket = models.ForeignKey(Ticket, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)

    
    def __str__(self):
        return f"Item in {self.cart}"