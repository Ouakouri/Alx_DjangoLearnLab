from django import forms

class MyForm(forms.Form):
    query = forms.CharField(max_length=100)
