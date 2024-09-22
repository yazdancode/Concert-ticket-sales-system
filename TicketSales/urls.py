from django.urls import path
from TicketSales.views import ConcertListView

urlpatterns = [
    path('concert/list/', ConcertListView, name='concert')
]
