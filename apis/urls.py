from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apis.views.user_profile import UserProfileRetrieveUpdateView
from apis.views.affiliate_profile import AffiliateProfileViewSet
from apis.views.affiliate_transaction import AffiliateTransactionViewSet
from apis.views.password_reset_request import PasswordResetRequestViewSet
from apis.views.otp_verification import OTPVerificationViewSet
from apis.views.affiliate_withdrawal import AffiliateWithdrawalViewSet
from apis.views.signup import UserSignUpView
from apis.views.signin import UserSignInView
from apis.views.competition_category import CompetitionCategoryViewSet
from apis.views.competition_image import CompetitionImageViewSet
from apis.views.competition import CompetitionViewSet  
from apis.views.ticket import TicketViewSet
from apis.views.ecard import ECardViewSet
from apis.views.instant_win_prize import InstantWinPrizeViewSet
from apis.views.winner import WinnerViewSet
from apis.views.ticket_by_letter import tickets_by_letter
from apis.views.cart import CartViewSet
from apis.views.cart_item import CartItemViewSet
from apis.views.order import OrderViewSet
from apis.views.order_item import OrderItemViewSet
from apis.views.product import ProductViewSet
from apis.views.product_category import ProductCategoryViewSet

router = DefaultRouter()
# router.register(r'user-profiles', UserProfileViewSet, basename='user-profile')
router.register(r'affiliates', AffiliateProfileViewSet, basename='affiliate')
router.register(r'affiliate-transactions', AffiliateTransactionViewSet, basename='affiliate-transaction')
router.register(r'affiliate-withdrawals', AffiliateWithdrawalViewSet, basename='affiliate-withdrawal')
router.register(r'otp', OTPVerificationViewSet, basename='otp')
router.register(r'password-reset', PasswordResetRequestViewSet, basename='password-reset')
router.register(r'categories', CompetitionCategoryViewSet)
router.register(r'competition-images', CompetitionImageViewSet)
router.register(r'competitions', CompetitionViewSet, basename='competition')  
router.register(r'tickets', TicketViewSet)
router.register(r'ecards', ECardViewSet)
router.register(r'instant-win-prizes', InstantWinPrizeViewSet)
router.register(r'winners', WinnerViewSet)
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cart-items')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'order-items', OrderItemViewSet, basename='order-items')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'categories', ProductCategoryViewSet, basename='categories')


urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('user-profiles/', UserProfileRetrieveUpdateView.as_view(), name='user-profile'),
    path('register/', UserSignUpView.as_view(), name='user-register'),
    path('login/', UserSignInView.as_view(), name='user-login'),
    path('competitions/<int:competition_id>/tickets/', tickets_by_letter, name='tickets-by-letter'),
]




