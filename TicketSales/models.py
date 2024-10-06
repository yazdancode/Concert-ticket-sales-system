from datetime import timedelta
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from jalali_date import date2jalali
from accounts.models import Profile


class ConcertStatus(models.TextChoices):
    AVAILABLE = "موجود است", "موجود است"
    SOLD_OUT = "فروخته شد", "فروخته شد"
    CANCELLED = "لغو شد", "لغو شد"


class Concert(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام کنسرت")
    singer_name = models.CharField(max_length=100, verbose_name="نام خواننده")
    length = models.IntegerField(
        verbose_name="مدت کنسرت (دقیقه)", validators=[MinValueValidator(1)]
    )
    Concert_picture = models.ImageField(
        upload_to="Concert_pictures/", verbose_name="عکس پروفایل", null=True, blank=True
    )
    date = models.DateTimeField(verbose_name="تاریخ و زمان کنسرت")
    location = models.CharField(max_length=255, verbose_name="محل برگزاری کنسرت")
    available_tickets = models.IntegerField(
        verbose_name="بلیط های موجود", validators=[MinValueValidator(0)]
    )
    ticket_price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="قیمت بلیط"
    )
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات کنسرت")
    ticket_status = models.CharField(
        max_length=10,
        choices=ConcertStatus.choices,
        default=ConcertStatus.AVAILABLE,
        verbose_name="وضعیت بلیط",
    )

    class Meta:
        verbose_name = "کنسرت"
        verbose_name_plural = "کنسرت"

    def __str__(self):
        return f"{self.name} by {self.singer_name} at {self.location}"


class Location(models.Model):
    id_number = models.IntegerField(primary_key=True, verbose_name="شماره شناسه")
    name = models.CharField(
        max_length=100,
        verbose_name="نام مکان",
        help_text="نام مکان را وارد کنید",
    )
    address = models.CharField(
        max_length=500,
        default="ایران-تهران",
        verbose_name="آدرس",
        help_text="آدرس کامل محل را وارد کنید",
    )
    phone = models.CharField(
        max_length=11,
        null=True,
        verbose_name="شماره تلفن",
        help_text="یک شماره تلفن معتبر وارد کنید",
        validators=[
            RegexValidator(
                regex=r"^\d{11}$",
                message="شماره تلفن باید ۱۱ رقم باشد",
            )
        ],
    )
    capacity = models.IntegerField(
        verbose_name="ظرفیت",
        help_text="حداکثر ظرفیت محل",
        validators=[MinValueValidator(1)],
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="عرض جغرافیایی",
        blank=True,
        null=True,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="طول جغرافیایی",
        blank=True,
        null=True,
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
    )
    WEBSITE_STATUS_CHOICES = [
        ("no_website", "وب‌سایت ندارد"),
        ("has_website", "وب‌سایت دارد"),
    ]
    website_status = models.CharField(
        max_length=20,
        verbose_name="وضعیت وب‌سایت",
        default="no_website",
        choices=WEBSITE_STATUS_CHOICES,
    )
    website = models.URLField(
        max_length=200, verbose_name="وب‌سایت", blank=True, null=True
    )
    opening_time = models.TimeField(verbose_name="زمان افتتاحیه", blank=True, null=True)
    closing_time = models.TimeField(verbose_name="زمان بسته شدن", blank=True, null=True)

    LOCATION_TYPE_CHOICES = [
        ("restaurant", "رستوران"),
        ("shop", "خرید کنید"),
        ("service_center", "مرکز خدمات"),
        ("concert", "کنسرت"),
    ]
    location_type = models.CharField(
        max_length=50, choices=LOCATION_TYPE_CHOICES, verbose_name="نوع مکان"
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال است")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="ایجاد شده در")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="به روز شده در")

    class Meta:
        verbose_name = "مکان"
        verbose_name_plural = "مکان‌ها"

    def clean(self):
        if self.website_status == "website" and not self.website:
            raise ValidationError("لطفاً آدرس وب‌سایت را وارد کنید.")
        if self.website_status == "no_website" and self.website:
            raise ValidationError(
                "وقتی گزینه 'وب‌سایت ندارد' را انتخاب می‌کنید، نباید آدرس وب‌سایت وارد شود."
            )
        if not self.is_active and (self.opening_time or self.closing_time):
            raise ValidationError(
                "برای مکان‌های غیرفعال نیازی به زمان افتتاح و بسته شدن نیست."
            )

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.PROTECT, verbose_name="کنسرت")
    location = models.ForeignKey(
        Location, on_delete=models.PROTECT, verbose_name="مکان"
    )
    start_date_time = models.DateTimeField(verbose_name="تاریخ و زمان شروع")
    end_date_time = models.DateTimeField(
        verbose_name="تاریخ و زمان پایان", blank=True, null=True
    )
    seats = models.IntegerField(
        verbose_name="تعداد صندلی", validators=[MinValueValidator(1)]
    )
    price_per_seat = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="قیمت هر صندلی",
        blank=True,
        null=True,
    )
    booked_seats = models.IntegerField(
        verbose_name="صندلی‌های رزرو شده", default=0, validators=[MinValueValidator(0)]
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال است")

    STATUS_CHOICES = [
        ("start", "شروع کنید"),
        ("end", "پایان"),
        ("sales", "فروش"),
        ("active", "فعال"),
        ("cancelled", "لغو شد"),
        ("completed", "تکمیل شد"),
    ]

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active", verbose_name="وضعیت"
    )
    remarks = models.TextField(blank=True, null=True, verbose_name="نکات تکمیلی")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="ایجاد شده در")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="به‌روز شده در")

    class Meta:
        verbose_name = "سانس"
        verbose_name_plural = "سانس‌ها"
        ordering = ["-start_date_time", "-end_date_time"]

    def clean(self):
        if self.end_date_time and self.start_date_time >= self.end_date_time:
            raise ValidationError("تاریخ پایان باید بعد از تاریخ شروع باشد.")
        if self.booked_seats > self.seats:
            raise ValidationError(
                "صندلی‌های رزرو شده نمی‌تواند بیشتر از تعداد صندلی‌ها باشد."
            )

    def save(self, *args, **kwargs):
        if not self.end_date_time:
            self.end_date_time = self.start_date_time + timedelta(
                minutes=self.concert.length
            )
        if self.price_per_seat is None:
            self.price_per_seat = Decimal("0.00")
        self.full_clean()
        super().save(*args, **kwargs)

    def get_jalai_date(self):
        return date2jalali(self.start_date_time), date2jalali(self.end_date_time)


class Ticket(models.Model):
    profilemodel = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        related_name="tickets",
        verbose_name="نمایه",
    )
    timemodel = models.ForeignKey(
        TimeSlot,
        on_delete=models.PROTECT,
        related_name="tickets",
        verbose_name="اسلات زمان",
    )
    name = models.CharField(max_length=1000, verbose_name="نام")
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="قیمت بلیط",
    )
    Ticket_picture = models.ImageField(
        upload_to="Ticket_pictures/", verbose_name="عکس پروفایل", null=True, blank=True
    )

    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ خرید")
    ticket_code = models.CharField(max_length=100, unique=True, verbose_name="کد بلیط")

    TICKET_STATUS_CHOICES = [
        ("active", "فعال"),
        ("expired", "منقضی"),
        ("canceled", "لغو شده"),
    ]
    ticket_status = models.CharField(
        max_length=10,
        choices=TICKET_STATUS_CHOICES,
        default="active",
        verbose_name="وضعیت بلیط",
    )

    reserved_seats = models.IntegerField(
        default=1, verbose_name="تعداد صندلی‌های رزرو شده"
    )
    expiration_date = models.DateTimeField(
        verbose_name="تاریخ انقضا", null=True, blank=True
    )

    PAYMENT_METHOD_CHOICES = [
        ("credit_card", "کارت اعتباری"),
        ("paypal", "PayPal"),
        ("cash", "نقدی"),
    ]
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="نحوه پرداخت"
    )

    additional_notes = models.TextField(
        blank=True, null=True, verbose_name="توضیحات اضافی"
    )

    class Meta:
        verbose_name = "بلیط"
        verbose_name_plural = "بلیط"

    def __str__(self):
        return f"{self.name} - {self.profilemodel.name} {self.profilemodel.family} (${self.price})"

