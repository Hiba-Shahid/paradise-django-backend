from django.contrib import admin
from .models import Competition, Ticket, Winner

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'prize_name', 'price_per_entry', 'total_tickets', 'remaining_tickets', 'status', 'start_date', 'end_date')
    list_filter = ('status',)
    search_fields = ('title', 'prize_name')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'user', 'competition', 'issued_at')
    search_fields = ('ticket_number', 'user__user__username')

@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'competition', 'prize', 'win_date', 'prize_status')
    list_filter = ('prize_status',)


