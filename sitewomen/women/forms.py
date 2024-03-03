from django import forms
from .models import Category, Husband

class AddPostForm(forms.Form):
    # класс для отображения формы редактирования записей
    # required=False для необязательных к заполнению полей
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea())
    is_published = forms.BooleanField()
    cat = forms.ModelChoiceField(queryset=Category.objects.all())
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False)
