from django.urls import path
from TicketSales.views import ConcertListView, locationListView

urlpatterns = [
    path('concert/list/', ConcertListView.as_view(), name='concert'),
    path('location/list/', locationListView, name='location')
]
