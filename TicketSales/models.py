from django.db import models
from django.core.validators import MinValueValidator
from datetime import timedelta


class ConcertStatus(models.TextChoices):
    AVAILABLE = "available", "Available"
    SOLD_OUT = "sold_out", "Sold Out"
    CANCELLED = "cancelled", "Cancelled"


class Concert(models.Model):
    name = models.CharField(max_length=100, verbose_name="Concert Name")
    singer_name = models.CharField(max_length=100, verbose_name="Singer Name")
    length = models.IntegerField(
        verbose_name="Concert Length (minutes)", validators=[MinValueValidator(1)]
    )
    date = models.DateTimeField(verbose_name="Concert Date and Time")
    location = models.CharField(max_length=255, verbose_name="Concert Location")
    available_tickets = models.IntegerField(
        verbose_name="Available Tickets", validators=[MinValueValidator(0)]
    )
    ticket_price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Ticket Price"
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Concert Description"
    )
    ticket_status = models.CharField(
        max_length=10,
        choices=ConcertStatus.choices,
        default=ConcertStatus.AVAILABLE,
        verbose_name="Ticket Status",
    )

    def __str__(self):
        return f"{self.name} by {self.singer_name} at {self.location}"


class Location(models.Model):
    id_number = models.IntegerField(primary_key=True)
    name = models.CharField(
        max_length=100,
        verbose_name="Location Name",
        help_text="Enter the name of the location",
    )
    address = models.CharField(
        max_length=500,
        default="Iran-Tehran",
        verbose_name="Address",
        help_text="Enter the full address of the location",
    )
    phone = models.CharField(
        max_length=11,
        null=True,
        verbose_name="Phone Number",
        help_text="Enter a valid phone number",
    )
    capacity = models.IntegerField(
        verbose_name="Capacity",
        help_text="Maximum capacity of the location",
        validators=[MinValueValidator(1)],
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name="Latitude", blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name="Longitude", blank=True, null=True
    )
    website = models.URLField(
        max_length=200, verbose_name="Website", blank=True, null=True
    )
    opening_time = models.TimeField(verbose_name="Opening Time", blank=True, null=True)
    closing_time = models.TimeField(verbose_name="Closing Time", blank=True, null=True)

    LOCATION_TYPE_CHOICES = [
        ("restaurant", "Restaurant"),
        ("shop", "Shop"),
        ("service_center", "Service Center"),
    ]

    location_type = models.CharField(
        max_length=50, choices=LOCATION_TYPE_CHOICES, verbose_name="Location Type"
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    concert = models.ForeignKey(
        "Concert", on_delete=models.PROTECT, verbose_name="Concert"
    )
    location = models.ForeignKey(
        "Location", on_delete=models.PROTECT, verbose_name="Location"
    )
    start_date_time = models.DateTimeField(verbose_name="Start Date and Time")
    end_date_time = models.DateTimeField(
        verbose_name="End Date and Time", blank=True, null=True
    )
    seats = models.IntegerField(
        verbose_name="Number of Seats", validators=[MinValueValidator(1)]
    )
    price_per_seat = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Price per Seat",
        blank=True,
        null=True,
    )
    booked_seats = models.IntegerField(
        verbose_name="Booked Seats", default=0, validators=[MinValueValidator(0)]
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    STATUS_CHOICES = [
        ("Start", "Start"),
        ("End", "End"),
        ("Sales", "Sales"),
        ("active", "Active"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active", verbose_name="Status"
    )
    remarks = models.TextField(blank=True, null=True, verbose_name="Additional Remarks")

    def clean(self):
        if self.end_date_time and self.start_date_time >= self.end_date_time:
            raise ValidationError("End date must be after the start date.")

    def save(self, *args, **kwargs):
        if not self.end_date_time:
            self.end_date_time = self.start_date_time + timedelta(
                minutes=self.concert.length
            )
        self.full_clean()
        super().save(*args, **kwargs)
