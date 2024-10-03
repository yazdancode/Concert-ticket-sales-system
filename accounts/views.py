from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView
from .forms import LoginForm, ProfileRegisterForm
from django.shortcuts import get_object_or_404, render
from accounts.models import Profile


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
        profileregisterform = ProfileRegisterForm(request.POST, request.FILES)
        if profileregisterform.is_valid():
            pass

    return render(request, "accounts/profileRegister.html")
