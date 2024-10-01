from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic import UpdateView

from TicketSales.forms import SearchForm, ConcertForm
from TicketSales.models import Concert, Location, TimeSlot


class ConcertListView(LoginRequiredMixin, ListView):
    model = Concert
    template_name = "TicketSales/concert_list.html"
    context_object_name = "concerts"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        searchform = SearchForm(self.request.GET)

        if searchform.is_valid():
            search_text = searchform.cleaned_data.get("SearchText")
            if search_text:
                queryset = queryset.filter(name__icontains=search_text)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["concertcount"] = self.get_queryset().count()
        context["searchform"] = SearchForm(self.request.GET)
        return context


class LocationListView(ListView):
    model = Location
    template_name = "TicketSales/location_list.html"
    context_object_name = "locationlist"


class ConcertDetailView(DetailView):
    model = Concert
    template_name = "TicketSales/consert_detail.html"  # اصلاح نام فایل
    context_object_name = "concertdetails"
    pk_url_kwarg = "concert_id"

    def get_object(self, queryset=None):
        concert_id = self.kwargs["concert_id"]
        return get_object_or_404(Concert, id=concert_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["concert_id"] = self.object.id  # Add concert_id to context
        return context


class TimeListView(LoginRequiredMixin, ListView):
    model = TimeSlot
    template_name = "TicketSales/timelist.html"
    context_object_name = "timelist"

    def get_queryset(self):
        return TimeSlot.objects.all()


class ConcertEditView(UpdateView):
    model = Concert
    form_class = ConcertForm
    template_name = "TicketSales/concert_edit.html"

    def get_success_url(self):
        return reverse("concert_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["concertForm"] = self.get_form()
        return context
