from rest_framework import serializers
from .models import Competition, Ticket,  Winner
from apis.models.user_profile import UserProfile

class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ['id', 'title', 'description', 'prize_name', 'prize_images', 'price_per_entry', 
                  'total_tickets', 'remaining_tickets', 'start_date', 'end_date', 'status', 'is_featured', 'created_at']

class TicketSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='user__username', queryset=UserProfile.objects.all())
    competition = serializers.SlugRelatedField(slug_field='title', queryset=Competition.objects.all())
    
    class Meta:
        model = Ticket
        fields = ['id', 'user', 'competition', 'ticket_number', 'issued_at']

class WinnerSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='user__username', queryset=UserProfile.objects.all())
    competition = serializers.SlugRelatedField(slug_field='title', queryset=Competition.objects.all())

    class Meta:
        model = Winner
        fields = ['id', 'user', 'competition', 'prize', 'win_date', 'prize_status']

