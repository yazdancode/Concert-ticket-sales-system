from django.urls import path
from .views import (
    ConcertListView,
    ConcertDetailView,
    ConcertEditView,
    LocationListView,
    TimeListView,
)

urlpatterns = [
    path("concerts/", ConcertListView.as_view(), name="concert_list"),
    path(
        "concerts/<int:concert_id>/", ConcertDetailView.as_view(), name="concert_detail"
    ),
    path(
        "concerts/<int:pk>/edit/", ConcertEditView.as_view(), name="concert_edit"
    ),  # Pass pk for editing
    path("locations/", LocationListView.as_view(), name="location_list"),
    path("timeslots/", TimeListView.as_view(), name="time_list"),
]
