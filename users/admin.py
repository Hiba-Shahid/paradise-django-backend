from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'phone', 'city', 'country')
    search_fields = ('user__username', 'email', 'phone')
    list_filter = ('country', 'city', 'created_at')
