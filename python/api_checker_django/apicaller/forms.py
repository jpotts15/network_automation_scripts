from django import forms

class ApiForm(forms.Form):
    api_url = forms.URLField(label='API URL', widget=forms.TextInput(attrs={'size': 50}))
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'size': 50}))
    password = forms.CharField(label='Password/Token', widget=forms.PasswordInput(attrs={'size': 50}))
