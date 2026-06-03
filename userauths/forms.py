from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Email",
            "required": "required",
            "class": "w-full bg-[#1A1A1A] border border-gray-700 rounded-md p-3 text-white placeholder-gray-400 focus:outline-none focus:border-accent"
        }),
        label=""
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "required": "required",
            "class": "w-full bg-[#1A1A1A] border border-gray-700 rounded-md p-3 text-white placeholder-gray-400 focus:outline-none focus:border-accent"
        }),
        label=""
    )
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "w-4 h-4 text-accent bg-gray-700 border-gray-600 rounded focus:ring-accent"}))

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Nama Lengkap",
        "class": "w-full bg-[#1A1A1A] border border-gray-700 rounded-md p-3 text-white placeholder-gray-400 focus:outline-none focus:border-accent"
    }), label="")
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "placeholder": "Email",
        "class": "w-full bg-[#1A1A1A] border border-gray-700 rounded-md p-3 text-white placeholder-gray-400 focus:outline-none focus:border-accent"
    }), label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "class": "w-full bg-[#1A1A1A] border border-gray-700 rounded-md p-3 text-white placeholder-gray-400 focus:outline-none focus:border-accent"
    }), label="")
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm Password",
        "class": "w-full bg-[#1A1A1A] border border-gray-700 rounded-md p-3 text-white placeholder-gray-400 focus:outline-none focus:border-accent"
    }), label="")

    class Meta:
        model = User
        fields = ['username', 'email']