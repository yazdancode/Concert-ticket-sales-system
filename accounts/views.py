from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView
from .forms import LoginForm, ProfileRegisterForm
from django.shortcuts import get_object_or_404, render
from accounts.models import Profile
from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponse


class CustomLoginView(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("time_list")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            next_url = self.request.GET.get("next")
            if next_url:
                return HttpResponseRedirect(next_url)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            context = self.get_context_data(form=form)
            context["username"] = username
            context["errorMessage"] = "کاربری با این مشخصات یافت نشد"
            return self.render_to_response(context)


class CustomLogoutView(RedirectView):
    url = reverse_lazy("concert_list")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "accounts/profile.html"
    context_object_name = "profile"

    def get_object(self, **kwargs):
        return get_object_or_404(Profile, user=self.request.user)


def ProfileRegisterView(request):
    if request.method == "POST":
        profile_register_form = ProfileRegisterForm(request.POST, request.FILES)
        if profile_register_form.is_valid():
            try:
                if User.objects.filter(
                    username=profile_register_form.cleaned_data["username"]
                ).exists():
                    profile_register_form.add_error(
                        "username", "این نام کاربری قبلاً ثبت شده است."
                    )

                elif User.objects.filter(
                    email=profile_register_form.cleaned_data["email"]
                ).exists():
                    profile_register_form.add_error(
                        "email", "این ایمیل قبلاً ثبت شده است."
                    )

                else:
                    user = User.objects.create_user(
                        username=profile_register_form.cleaned_data["username"],
                        email=profile_register_form.cleaned_data["email"],
                        password=profile_register_form.cleaned_data["password"],
                        first_name=profile_register_form.cleaned_data["first_name"],
                        last_name=profile_register_form.cleaned_data["last_name"],
                    )
                    user.save()
                    profile = Profile(
                        user=user,
                        profile_picture=profile_register_form.cleaned_data[
                            "profile_picture"
                        ],
                        gender=profile_register_form.cleaned_data["gender"],
                        credit=profile_register_form.cleaned_data["credit"],
                    )
                    profile.save()

                    return HttpResponseRedirect(reverse("concert_list"))

            except IntegrityError as e:
                return HttpResponse(f"خطا: {str(e)}")
    else:
        profile_register_form = ProfileRegisterForm()

    context = {"form": profile_register_form}
    return render(request, "accounts/profileRegister.html", context)
