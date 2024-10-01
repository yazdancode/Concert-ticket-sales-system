from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView
from TicketSales.forms import SearchForm, ConcertForm
from TicketSales.models import Concert, Location, TimeSlot


class ConcertListView(LoginRequiredMixin, ListView):
    model = Concert
    template_name = "TicketSales/concert_list.html"
    context_object_name = "concerts"
    paginate_by = 10

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
    template_name = "TicketSales/location_list.html"
    context_object_name = "locationlist"


class ConcertDetailView(DetailView):
    model = Concert
    template_name = "TicketSales/consert_detail.html"
    context_object_name = "concertdetails"
    pk_url_kwarg = "concert_id"

    def get_object(self, queryset=None):
        return get_object_or_404(Concert, id=self.kwargs["concert_id"])


class TimeListView(LoginRequiredMixin, ListView):
    model = TimeSlot
    template_name = "TicketSales/timelist.html"
    context_object_name = "timelist"

    def get_queryset(self):
        return TimeSlot.objects.all()


class ConcertEditView(LoginRequiredMixin, UpdateView):
    model = Concert
    form_class = ConcertForm
    template_name = "TicketSales/concert_edit.html"
    success_url = reverse_lazy("concert")

    def get_object(self, queryset=None):
        concert_id = self.kwargs["concert_id"]
        return get_object_or_404(Concert, id=concert_id)

    def form_valid(self, form):
        messages.success(self.request, "Concert updated successfully!")
        return super().form_valid(form)
