from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

# 1. FORM UNTUK HALAMAN ENTRY
class UserEntryForm(forms.Form):
    identifier = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Email atau Nomor WhatsApp",
            "required": "required"
        }),
        label=""
    )

# 2. FORM UNTUK HALAMAN LOGIN
class UserLoginForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "required": "required"
        }),
        label=""
    )

# 3. FORM UNTUK HALAMAN REGISTER (Sudah dibuat sebelumnya)
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nama Lengkap"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nomor WhatsApp"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']