from django.contrib import admin
from apis.models.competition import Competition
from apis.models.ticket import Ticket
from apis.models.competition_category import CompetitionCategory

# Register your models here.
admin.site.register(CompetitionCategory)
admin.site.register(Competition)
admin.site.register(Ticket)