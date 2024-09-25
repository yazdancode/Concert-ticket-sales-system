from django.urls import path
from TicketSales.views import ConcertListView, LocationListView, ConcertDetailView

urlpatterns = [
    path("concert/list/", ConcertListView.as_view(), name="concert"),
    path("location/list/", LocationListView.as_view(), name="location"),
    path(
        "concert/<int:concert_id>/", ConcertDetailView.as_view(), name="concert_detail"
    ),
]
