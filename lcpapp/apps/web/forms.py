from django.forms import BaseForm, Form
from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _

def set_form_fields_disabled(form: BaseForm, disabled: bool = True) -> None:
    """
    For a given form, disable (or enable) all fields.
    """
    for field in form.fields:
        form.fields[field].disabled = disabled

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-input',
                'placeholder': _('Enter your email'),
                'autocomplete': 'email',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': _('Enter your password'),
                'autocomplete': 'current-password',
            }
        )
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-checkbox',
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError(
                    _('Invalid email or password. Please try again.'),
                    code='invalid_login'
                )
            elif not user.is_active:
                raise forms.ValidationError(
                    _('This account is inactive. Please contact support.'),
                    code='inactive'
                )
            cleaned_data['user'] = user

        return cleaned_data
