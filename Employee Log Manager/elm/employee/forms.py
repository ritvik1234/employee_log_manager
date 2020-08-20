from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth import password_validation

class Registeration(forms.Form):
    name = forms.CharField(validators=[RegexValidator(r'[a-zA-Z]+', 'Enter a valid first name(only letters)')])
    email = forms.EmailField(label='E-mail')
    username = forms.CharField()
    password = forms.CharField(max_length=32, widget=forms.PasswordInput, help_text = password_validation.password_validators_help_text_html())
    repass = forms.CharField(label ='Password confirmation', max_length=32, widget=forms.PasswordInput)
    rate = forms.IntegerField()

    def clean(self):
        if self.cleaned_data.get('password')!= self.cleaned_data.get('repass'):
            raise forms.ValidationError('Passwords are not equal')
        password_validation.validate_password(self.cleaned_data.get('password'), None)
        return self.cleaned_data
class Register(forms.Form):
    name = forms.CharField(validators=[RegexValidator(r'[a-zA-Z]+', 'Enter a valid first name(only letters)')])
    email = forms.EmailField(label='E-mail')
    rate = forms.IntegerField()
