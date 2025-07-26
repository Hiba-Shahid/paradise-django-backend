from django.contrib import admin
from apis.models.competition import Competition
from apis.models.ticket import Ticket
from apis.models.competition_category import CompetitionCategory
from apis.models.cart import Cart
from apis.models.cart_item import CartItem
from apis.models.order import Order
from apis.models.order_item import OrderItem
from apis.models.product import Product
from apis.models.product_category import ProductCategory
from apis.models.order import Order

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['sale_code', 'created_at']
    list_display = ['sale_code', 'user_profile', 'total_amount', 'payment_method', 'created_at']
    search_fields = ['sale_code', 'user_profile_user_username']
    list_filter = ['payment_method', 'created_at']


admin.site.register(CompetitionCategory)
admin.site.register(Competition)
admin.site.register(Ticket)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Order,OrderAdmin)