from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    # username = forms.CharField(label= 'Логин',
    #                            widget=forms.TextInput(attrs={'class': 'form-input'}))
    # password = forms.CharField(label= 'Пароль',
    #                            widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model() # привязка к стандартной модели пользователя
        fields = ['username','password'] # указывает поля для отображения в форме

class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля',widget=forms.PasswordInput())

    class Meta:
        model= get_user_model()
        fields = ['username', 'email','first_name','last_name','password','password2',]
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }