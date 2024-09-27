from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from TicketSales.models import Concert, Location, TimeSlot
from accounts.views import CustomLoginView
from django.urls import reverse


class ConcertListView(ListView):
    model = Concert
    template_name = "TicketSales/concert_list.html"
    context_object_name = "concerts"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["concertcount"] = self.get_queryset().count()
        return context


class LocationListView(ListView):
    model = Location
    template_name = "TicketSales/locationlist.html"
    context_object_name = "locationlist"


class ConcertDetailView(DetailView):
    model = Concert
    template_name = "TicketSales/consert-detail.html"
    context_object_name = "concertdetails"
    pk_url_kwarg = "concert_id"


class TimeListView(LoginRequiredMixin, ListView):
    model = TimeSlot
    template_name = "TicketSales/timelist.html"
    context_object_name = "timelist"

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_active:
            return TimeSlot.objects.all()
        else:
            return HttpResponseRedirect(reverse(CustomLoginView))
