from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginUserForm(AuthenticationForm):
    # username = forms.CharField(label= 'Логин',
    #                            widget=forms.TextInput(attrs={'class': 'form-input'}))
    # password = forms.CharField(label= 'Пароль',
    #                            widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model() # привязка к стандартной модели пользователя
        fields = ['username','password'] # указывает поля для отображения в форме

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    password1 = forms.CharField(label='Пароль',widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля',widget=forms.PasswordInput())

    class Meta:
        model= get_user_model()
        fields = ['username', 'email','first_name','last_name','password1','password2',]
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }
        widgets = {
                   'email': forms.TextInput(attrs={'class': 'form-input'}),
                   'first_name': forms.TextInput(attrs={'class': 'form-input'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }
    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError('Пароли не совпадают')
    #     return cd['password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой e-mail уже существует')
        return email

class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label= 'Логин',widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label= 'E-mail',widget=forms.TextInput(attrs={'class': 'form-input'}))
    class Meta:
        model= get_user_model()
        fields = ['username', 'email','first_name','last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }
        widgets = {
                   'first_name': forms.TextInput(attrs={'class': 'form-input'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }