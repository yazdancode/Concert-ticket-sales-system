from django import forms


class SearchForm(forms.Form):
    SearchText = forms.CharField(max_length=256, label="نام کنسرت", required=False)
