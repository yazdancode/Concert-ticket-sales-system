# Generated by Django 5.1.1 on 2024-10-05 13:18

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Concert",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="نام کنسرت")),
                (
                    "singer_name",
                    models.CharField(max_length=100, verbose_name="نام خواننده"),
                ),
                (
                    "length",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="مدت کنسرت (دقیقه)",
                    ),
                ),
                (
                    "Concert_picture",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="Concert_pictures/",
                        verbose_name="عکس پروفایل",
                    ),
                ),
                ("date", models.DateTimeField(verbose_name="تاریخ و زمان کنسرت")),
                (
                    "location",
                    models.CharField(max_length=255, verbose_name="محل برگزاری کنسرت"),
                ),
                (
                    "available_tickets",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="بلیط های موجود",
                    ),
                ),
                (
                    "ticket_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=8, verbose_name="قیمت بلیط"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="توضیحات کنسرت"
                    ),
                ),
                (
                    "ticket_status",
                    models.CharField(
                        choices=[
                            ("موجود است", "موجود است"),
                            ("فروخته شد", "فروخته شد"),
                            ("لغو شد", "لغو شد"),
                        ],
                        default="موجود است",
                        max_length=10,
                        verbose_name="وضعیت بلیط",
                    ),
                ),
            ],
            options={
                "verbose_name": "کنسرت",
                "verbose_name_plural": "کنسرت",
            },
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id_number",
                    models.IntegerField(
                        primary_key=True, serialize=False, verbose_name="شماره شناسه"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="نام مکان را وارد کنید",
                        max_length=100,
                        verbose_name="نام مکان",
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        default="ایران-تهران",
                        help_text="آدرس کامل محل را وارد کنید",
                        max_length=500,
                        verbose_name="آدرس",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        help_text="یک شماره تلفن معتبر وارد کنید",
                        max_length=11,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="شماره تلفن باید ۱۱ رقم باشد", regex="^\\d{11}$"
                            )
                        ],
                        verbose_name="شماره تلفن",
                    ),
                ),
                (
                    "capacity",
                    models.IntegerField(
                        help_text="حداکثر ظرفیت محل",
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="ظرفیت",
                    ),
                ),
                (
                    "latitude",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        max_digits=9,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(-90.0),
                            django.core.validators.MaxValueValidator(90.0),
                        ],
                        verbose_name="عرض جغرافیایی",
                    ),
                ),
                (
                    "longitude",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        max_digits=9,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(-180.0),
                            django.core.validators.MaxValueValidator(180.0),
                        ],
                        verbose_name="طول جغرافیایی",
                    ),
                ),
                (
                    "website_status",
                    models.CharField(
                        choices=[
                            ("no_website", "وب\u200cسایت ندارد"),
                            ("has_website", "وب\u200cسایت دارد"),
                        ],
                        default="no_website",
                        max_length=20,
                        verbose_name="وضعیت وب\u200cسایت",
                    ),
                ),
                (
                    "website",
                    models.URLField(blank=True, null=True, verbose_name="وب\u200cسایت"),
                ),
                (
                    "opening_time",
                    models.TimeField(
                        blank=True, null=True, verbose_name="زمان افتتاحیه"
                    ),
                ),
                (
                    "closing_time",
                    models.TimeField(
                        blank=True, null=True, verbose_name="زمان بسته شدن"
                    ),
                ),
                (
                    "location_type",
                    models.CharField(
                        choices=[
                            ("restaurant", "رستوران"),
                            ("shop", "خرید کنید"),
                            ("service_center", "مرکز خدمات"),
                            ("concert", "کنسرت"),
                        ],
                        max_length=50,
                        verbose_name="نوع مکان",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="فعال است"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="ایجاد شده در"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="به روز شده در"),
                ),
            ],
            options={
                "verbose_name": "مکان",
                "verbose_name_plural": "مکان\u200cها",
            },
        ),
        migrations.CreateModel(
            name="TimeSlot",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "start_date_time",
                    models.DateTimeField(verbose_name="تاریخ و زمان شروع"),
                ),
                (
                    "end_date_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="تاریخ و زمان پایان"
                    ),
                ),
                (
                    "seats",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="تعداد صندلی",
                    ),
                ),
                (
                    "price_per_seat",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=8,
                        null=True,
                        verbose_name="قیمت هر صندلی",
                    ),
                ),
                (
                    "booked_seats",
                    models.IntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="صندلی\u200cهای رزرو شده",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="فعال است"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("start", "شروع کنید"),
                            ("end", "پایان"),
                            ("sales", "فروش"),
                            ("active", "فعال"),
                            ("cancelled", "لغو شد"),
                            ("completed", "تکمیل شد"),
                        ],
                        default="active",
                        max_length=10,
                        verbose_name="وضعیت",
                    ),
                ),
                (
                    "remarks",
                    models.TextField(blank=True, null=True, verbose_name="نکات تکمیلی"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="ایجاد شده در"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="به\u200cروز شده در"
                    ),
                ),
                (
                    "concert",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="TicketSales.concert",
                        verbose_name="کنسرت",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="TicketSales.location",
                        verbose_name="مکان",
                    ),
                ),
            ],
            options={
                "verbose_name": "سانس",
                "verbose_name_plural": "سانس\u200cها",
                "ordering": ["-start_date_time", "-end_date_time"],
            },
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=1000, verbose_name="نام")),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=8,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="قیمت بلیط",
                    ),
                ),
                (
                    "Ticket_picture",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="Ticket_pictures/",
                        verbose_name="عکس پروفایل",
                    ),
                ),
                (
                    "purchase_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="تاریخ خرید"),
                ),
                (
                    "ticket_code",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="کد بلیط"
                    ),
                ),
                (
                    "ticket_status",
                    models.CharField(
                        choices=[
                            ("active", "فعال"),
                            ("expired", "منقضی"),
                            ("canceled", "لغو شده"),
                        ],
                        default="active",
                        max_length=10,
                        verbose_name="وضعیت بلیط",
                    ),
                ),
                (
                    "reserved_seats",
                    models.IntegerField(
                        default=1, verbose_name="تعداد صندلی\u200cهای رزرو شده"
                    ),
                ),
                (
                    "expiration_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="تاریخ انقضا"
                    ),
                ),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("credit_card", "کارت اعتباری"),
                            ("paypal", "PayPal"),
                            ("cash", "نقدی"),
                        ],
                        max_length=20,
                        verbose_name="نحوه پرداخت",
                    ),
                ),
                (
                    "additional_notes",
                    models.TextField(
                        blank=True, null=True, verbose_name="توضیحات اضافی"
                    ),
                ),
                (
                    "profilemodel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="tickets",
                        to="accounts.profile",
                        verbose_name="نمایه",
                    ),
                ),
                (
                    "timemodel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="tickets",
                        to="TicketSales.timeslot",
                        verbose_name="اسلات زمان",
                    ),
                ),
            ],
            options={
                "verbose_name": "بلیط",
                "verbose_name_plural": "بلیط",
            },
        ),
    ]
