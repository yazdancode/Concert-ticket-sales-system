from django.shortcuts import render
from TicketSales.models import Concert

def ConcertListView(request):
    concert = Concert.objects.all()
    context = {
        'concerts': concert,
        'concertcount': concert.count(),
    }
    return render(request, 'TicketSales/concert_list.html', context)
