from django.urls import path

from accounts.views import (
    CustomLoginView,
    CustomLogoutView,
    ProfileView,
    ProfileRegisterView,
)

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("register/", ProfileRegisterView, name="profile-register"),
]
