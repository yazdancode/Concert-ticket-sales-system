from django.views.generic import ListView
from TicketSales.models import Concert, Location

class ConcertListView(ListView):
    model = Concert
    template_name = 'TicketSales/concert_list.html'
    context_object_name = 'concerts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['concertcount'] = self.get_queryset().count()
        return context
    
class LocationListView(ListView):
    model = Location
    template_name = 'TicketSales/locationlist.html'
    context_object_name = 'locations'
    paginate_by = 10
    
    
    



