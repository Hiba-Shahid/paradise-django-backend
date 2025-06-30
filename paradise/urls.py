from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/competition/', include('competition.urls')),
    path('api/giftshop/', include('giftshop.urls')),

    # Include login endpoint from main app
    path('api/auth/', include('main.urls')),  # 🔴 This is now main.urls
]
