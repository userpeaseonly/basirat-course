from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    phone_number = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': _('+998901234567')
        }),
        label=_('Phone number')
    )

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'is_student')


class CustomUserChangeForm(UserChangeForm):
    phone_number = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': _('+998901234567')
        }),
        label=_('Phone number')
    )

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'is_student')


class CustomAuthenticationForm(AuthenticationForm):
    username = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': _('+998901234567')
        }),
        label=_('Phone number')
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': _('Password')
        }),
        label=_('Password')
    )


class QuickCreateAccountForm(forms.Form):
    phone_number = PhoneNumberField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': _('Phone Number (any format)')
        }),
        label=_('Phone number'),
        help_text=_('The number is validated by the phone-number field but no OTP is sent.')
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': _('Password')
        }),
        label=_('Password')
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': _('Confirm password')
        }),
        label=_('Confirm password')
    )
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('Passwords do not match.'))
        return cleaned_data

    def save(self):
        return CustomUser.objects.create_user(
            phone_number=self.cleaned_data['phone_number'],
            password=self.cleaned_data['password1'],
            is_student=True
        )
