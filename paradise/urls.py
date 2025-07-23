from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.permissions import AllowAny

# Swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from rest_framework.authentication import TokenAuthentication
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Paradise API",
        default_version='v1',
        description="API documentation for Paradise project",
    ),
    public=True,
    permission_classes=(AllowAny,),
    authentication_classes=(TokenAuthentication,),  
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/giftshop/', include('giftshop.urls')),
    path('api/token/', obtain_auth_token),
    path('api/', include('apis.urls')),

    # Swagger & Redoc URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
