from django import forms

class SearchBar(forms.Form):
    keyword = forms.CharField()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)