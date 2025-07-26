from rest_framework import serializers
from apis.models.product import Product

class ProductSerializer(serializers.ModelSerializer):
    is_digital = serializers.ReadOnlyField()
    is_out_of_stock = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'product_type',
            'file', 'image', 'stock', 'price', 'is_active',
            'category', 'is_featured_homepage', 'is_general_ecard',
            'competition_link', 'is_digital', 'is_out_of_stock'
        ]
        read_only_fields = ['id', 'is_digital', 'is_out_of_stock']
