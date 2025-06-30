from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/competition/', include('competition.urls')),
    path('api/giftshop/', include('giftshop.urls')),
    path('api/auth/', include('main.urls')),
    path('api/account/', include('main.urls')),  
]
