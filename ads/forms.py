from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ad


class RegisterForm(UserCreationForm):
    """Форма регистрации — стандартная джанговская + красивые подписи."""

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class AdForm(forms.ModelForm):
    """Форма создания и редактирования объявления."""

    class Meta:
        model = Ad
        fields = ['title', 'price', 'description', 'category', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
