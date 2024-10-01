from django.urls import path
from TicketSales.views import (
    ConcertListView,
    LocationListView,
    ConcertDetailView,
    TimeListView,
    ConcertEditView,
)

urlpatterns = [
    path("concert/list/", ConcertListView.as_view(), name="concert"),
    path("location/list/", LocationListView.as_view(), name="location"),
    path(
        "concert/<int:concert_id>/", ConcertDetailView.as_view(), name="concert_detail"
    ),
    path("time/list/", TimeListView.as_view(), name="time_list"),
    path(
        "concert_Form/<int:concert_id>/", ConcertEditView.as_view(), name="concert_Form"
    ),
]
