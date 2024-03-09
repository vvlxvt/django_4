from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Women


@deconstructible
class RussianValidator:
    # свой валидатор который проверяет, что заголовок написан на русском языке
    ALLOWED_CHARS= 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёдзийклмнопрстуфхцчшщъыьэюя0123456789-'
    code = 'russian'

    def __init__(self, message = None):
        self.message = message if message else "должны присутствовать только русские буквы, цифры"

    def __call__(self,value, *args, **kwargs):
        # проверка символов на соответствие ALLOWED_CHARS
        # метод позволяет использовать экземпляр класса как функцию
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code = self.code)

class AddPostForm(forms.ModelForm):

    cat = forms.ModelChoiceField(queryset=Category.objects.all(),label='Категория', empty_label='не указано')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label='Муж', empty_label='не замужем')

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'is_published', 'cat', 'husband','tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms. Textarea(attrs={'cols': 50, 'rows': 5})
        }
        labels = {'slug': 'URL'}

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Файл')
    file = forms.ImageField(label='Файл')








    def clean_title(self):
        # так можно прописать валидатор если он используется с одним полем
        # получаем значение из словаря с ключом "title"
        title = self.cleaned_data['title']
        # указываем допустимые символы
        ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёдзийклмнопрстуфхцчшщъыьэюя0123456789-'
        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError("Должны присутствовать только русские буквы, цифры")
        elif len(title)> 50:
            raise ValidationError("Длина превышает 50 символов")
        return title

