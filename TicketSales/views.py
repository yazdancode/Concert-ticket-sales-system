from blib2to3.pytree import convert
from django.shortcuts import render
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
    
def locationListView(request):
    locations=Location.objects.all()
    context={
        "locationlist":locations,
    }
    return render(request, 'TicketSales/locationlist.html', context)
    
    
    



