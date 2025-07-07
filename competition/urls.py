from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompetitionViewSet, TicketViewSet, WinnerViewSet

router = DefaultRouter()
router.register(r'competitions', CompetitionViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'winners', WinnerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
