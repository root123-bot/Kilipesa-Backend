from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class ChangePassword(PasswordChangeForm):
    """ChangePassword definition."""

    # TODO: Define form fields
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=50, label="New password", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'New password'}))
    new_password2 = forms.CharField(max_length=50, label="Confirm password", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Confirm password'}))

    class Meta:
        model = get_user_model()
        fields = ('old_password', 'new_password1', 'new_password2')
