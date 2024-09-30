from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from TicketSales.forms import SearchForm
from TicketSales.models import Concert, Location, TimeSlot


class ConcertListView(ListView):
    model = Concert
    template_name = "TicketSales/concert_list.html"
    context_object_name = "concerts"
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        context["concertcount"] = self.get_queryset().count()
        searchform = SearchForm(request.GET)
        context["searchform"] = searchform

        if searchform.is_valid():
            search_text = searchform.cleaned_data["SearchText"]
            concerts = Concert.objects.filter(name__icontains=search_text)
        else:
            concerts = Concert.objects.all()
        context["concerts"] = concerts
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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_active:
            return super().dispatch(*args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("custom_login"))

    def get_queryset(self):
        return TimeSlot.objects.all()
