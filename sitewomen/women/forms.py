from django import forms
from .models import Category, Husband

class AddPostForm(forms.Form):
    # класс для отображения формы редактирования записей
    # required=False для необязательных к заполнению полей
    title = forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={'class':'form-input'}))
    slug = forms.SlugField(max_length=255, label='URL')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols':50, 'rows':5}), label='Содержание')
    is_published = forms.BooleanField(label='Опубликовано', initial = True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),label='Категория', empty_label='не указано')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label='Муж', empty_label='не '
                                                                                                              'замужем')
