from django import forms
from .models import Info


class InfoForm(forms.ModelForm):
    other = forms.CharField(widget=forms.Textarea(
        attrs={'cols': '45', 'rows': '6'}),
        label='Other contacts')
    bio = forms.CharField(widget=forms.Textarea(
        attrs={'cols': '45', 'rows': '6'}), label='Biography')
    dob = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'datepicker'}), label='Date of birth')
    photo = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Info
