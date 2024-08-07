from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']
        




class TransitionForm(forms.Form):
    money = forms.CharField(label='Перевод')
    commentary = forms.CharField(label='Сообщение', max_length=100, required=False)

    def clean_money(self):
        data = self.cleaned_data['money']
        data = "".join(data.split("."))
        # Ваша логика валидации
        if int(data) < 50:
            raise forms.ValidationError("Invalid username")
        return int(data)