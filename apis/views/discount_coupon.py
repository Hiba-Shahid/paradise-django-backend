from rest_framework import viewsets
from apis.models.discount_coupon import DiscountCoupon
from apis.serializers.discount_coupon import DiscountCouponSerializer

class DiscountCouponViewSet(viewsets.ReadOnlyModelViewSet):
    
    queryset = DiscountCoupon.objects.all()
    serializer_class = DiscountCouponSerializer
    lookup_field = 'code' 

    def get_queryset(self):
        queryset = self.queryset

        active = self.request.query_params.get('active')
        if active is not None:
            queryset = queryset.filter(active=active.lower() == 'true')

        return queryset
