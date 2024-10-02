from django import forms

from TicketSales.models import Concert


class SearchForm(forms.Form):
    SearchText = forms.CharField(max_length=256, label="نام کنسرت", required=False)


class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ["name", "singer_name", "length", "Concert_picture"]

    def __init__(self, *args, **kwargs):
        super(ConcertForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "mylable", "placeholder": "نام کنسرت"}
        )
        self.fields["singer_name"].widget.attrs.update(
            {"class": "mylable", "placeholder": "نام خواننده"}
        )
        self.fields["length"].widget.attrs.update(
            {"class": "mylable", "placeholder": "مدت زمان"}
        )
        self.fields["Concert_picture"].widget.attrs.update({"class": "mylable"})

    # def clean_Concert_picture(self):
    #     image = self.cleaned_data.get("Concert_picture")
    #     if image:
    #         if image.size > 5 * 1024 * 1024:
    #             raise forms.ValidationError("سایز عکس باید کمتر از 5 مگابایت باشد.")
    #         if not image.content_type in ["image/jpeg", "image/png"]:
    #             raise forms.ValidationError(
    #                 "فایل باید یک عکس با فرمت JPEG یا PNG باشد."
    #             )
    #         return image
