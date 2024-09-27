from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from .forms import LoginForm


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
            return HttpResponseRedirect(reverse_lazy("time_list"))
        else:
            context = self.get_context_data(form=form)
            context["username"] = username
            context["errorMessage"] = "کاربری با این مشخصات یافت نشد"
            return self.render_to_response(context)
