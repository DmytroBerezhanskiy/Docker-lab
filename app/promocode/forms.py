from django import forms


class PromocodeForm(forms.Form):
    code = forms.CharField()