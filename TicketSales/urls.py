from django.urls import path
from TicketSales.views import ConcertListView, LocationListView

urlpatterns = [
    path('concert/list/', ConcertListView.as_view(), name='concert'),
    path('location/list/', LocationListView.as_view(), name='location')
]
