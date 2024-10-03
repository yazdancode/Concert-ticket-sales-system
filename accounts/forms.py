from django import forms
from accounts.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(
        label="نام کاربری",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-group", "placeholder": "نام کاربری"}
        ),
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={"class": "form-group", "placeholder": "رمز عبور"}
        ),
    )


class ProfileRegisterForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        label="نام کاربری",
        widget=forms.TextInput(
            attrs={"class": "form-group", "placeholder": "نام کاربری"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-group", "placeholder": "رمز عبور"}
        ),
        label="رمز عبور",
    )
    first_name = forms.CharField(
        max_length=256,
        label="نام",
        widget=forms.TextInput(attrs={"class": "form-group", "placeholder": "نام"}),
    )
    last_name = forms.CharField(
        max_length=256,
        label="نام خانوادگی",
        widget=forms.TextInput(
            attrs={"class": "form-group", "placeholder": "نام خانوادگی"}
        ),
    )
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(attrs={"class": "form-group", "placeholder": "ایمیل"}),
    )

    class Meta:
        model = Profile
        fields = ["Credit", "gender", "profile_picture"]

    def __init__(self, *args, **kwargs):
        super(ProfileRegisterForm, self).__init__(*args, **kwargs)
