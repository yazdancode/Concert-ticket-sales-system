from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="کاربری", related_name="profile"
    )
    # name = models.CharField(max_length=100, verbose_name="نام")
    # family = models.CharField(max_length=100, verbose_name="نام خانوادگی")

    STATUS_CHOICES = [
        ("Man", "مرد"),
        ("Woman", "زن"),
    ]

    gender = models.CharField(
        max_length=6,
        choices=STATUS_CHOICES,
        verbose_name="جنسیت",
    )

    birth_date = models.DateField(verbose_name="تاریخ تولد", null=True, blank=True)
    email = models.EmailField(verbose_name="آدرس ایمیل", unique=True, max_length=100)
    phone_number = models.CharField(
        max_length=15, verbose_name="شماره تلفن", null=True, blank=True
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", verbose_name="عکس پروفایل", null=True, blank=True
    )
    bio = models.TextField(verbose_name="بیوگرافی", blank=True, max_length=255)
    address = models.CharField(
        max_length=255, verbose_name="آدرس", null=True, blank=True
    )
    credit = models.IntegerField(verbose_name="اعتبار", default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت‌ نام")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین بروزرسانی"
    )

    class Meta:
        verbose_name = "نمایه"
        verbose_name_plural = "نمایه"

    def __str__(self):
        return f"{self.gender}"
