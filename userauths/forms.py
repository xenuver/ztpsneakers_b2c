from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Email",
            "required": "required",
            "class": "w-full bg-white border border-gray-300 rounded-md p-3 text-black placeholder-gray-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black"
        }),
        label=""
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "required": "required",
            "class": "w-full bg-white border border-gray-300 rounded-md p-3 text-black placeholder-gray-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black"
        }),
        label=""
    )
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "w-4 h-4 text-black bg-white border-gray-300 rounded focus:ring-black"}))

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Nama Lengkap",
        "class": "w-full bg-white border border-gray-300 rounded-md p-3 text-black placeholder-gray-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black"
    }), label="")
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "placeholder": "Email",
        "class": "w-full bg-white border border-gray-300 rounded-md p-3 text-black placeholder-gray-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black"
    }), label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "class": "w-full bg-white border border-gray-300 rounded-md p-3 text-black placeholder-gray-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black"
    }), label="")
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm Password",
        "class": "w-full bg-white border border-gray-300 rounded-md p-3 text-black placeholder-gray-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black"
    }), label="")

    class Meta:
        model = User
        fields = ['username', 'email']