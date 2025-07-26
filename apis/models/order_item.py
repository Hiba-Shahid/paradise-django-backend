from django.db import models
from apis.models.order import Order
from apis.models.product import Product
from apis.models.ticket import Ticket


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    ticket = models.ForeignKey(Ticket, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Item in Order #{self.order.sale_code}"