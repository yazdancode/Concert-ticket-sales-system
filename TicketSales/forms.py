from django import forms
from TicketSales.models import Concert


class SearchForm(forms.Form):
    SearchText = forms.CharField(max_length=256, label="نام کنسرت", required=False)


class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ["name", "singer_name", "length", "Concert_picture"]
        # exclude = ["Concert_picture"]
