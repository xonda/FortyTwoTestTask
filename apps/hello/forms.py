from django import forms
from .models import Info


class InfoForm(forms.ModelForm):
    other = forms.CharField(widget=forms.Textarea(
        attrs={'cols': '45', 'rows': '6'}),
        label='Other contacts', required=True)
    bio = forms.CharField(widget=forms.Textarea(
        attrs={'cols': '45', 'rows': '6'}), label='Biography', required=True)
    surname = forms.CharField(label='Last name')
    dob = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'datepicker'}), label='Date of birth', required=True)
    email = forms.EmailField(required=True)
    jabber = forms.CharField(required=True)
    skype = forms.CharField(required=True)

    class Meta:
        model = Info
