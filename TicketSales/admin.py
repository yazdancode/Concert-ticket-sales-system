from django.contrib import admin
from TicketSales.models import (
    Concert,
    Location,
    TimeSlot,
    Profile,
    Ticket,
)

admin.site.register(Concert)
admin.site.register(Location)
admin.site.register(TimeSlot)
admin.site.register(Profile)
admin.site.register(Ticket)
