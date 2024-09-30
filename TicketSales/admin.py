from django.contrib import admin
from TicketSales.models import (
    Concert,
    Location,
    TimeSlot,
    Ticket,
)

admin.site.register(Concert)
admin.site.register(Location)
admin.site.register(TimeSlot)
admin.site.register(Ticket)
