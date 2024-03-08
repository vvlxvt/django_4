from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from .forms import AddPostForm
from .models import Women, Category, TagPost

menu = [
    {'title': 'О сайте', 'url_name': "about"},
    {'title': "Добавить статью", 'url_name': "addpage"},
    {'title': "Обратная связь", 'url_name':'contact'},
    {'title': "Войти", 'url_name': 'login'}
]

# Create your views here.
def index(request):
    # метод "select_related" жадная загрузка связанных по внешнему ключу даннных типа Foreign key()
    posts = Women.published.all().select_related('cat')
    print(posts)
    data = {
        'title': 'главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
        }
    return render(request, 'women/index.html', context = data)

def about(request):
    return render(request, 'women/about.html', {'title':'О сайте', 'menu': menu})

def show_post(request, post_slug):
    post = get_object_or_404(Women, slug = post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
        }
    return render(request, 'women/post.html', data)

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug = cat_slug)
    posts = Women.published.filter(cat_id = category.pk).select_related('cat')
    data = {'title': f'Рубрика: {category.name}',
            'menu': menu,
            'posts': posts,
            'cat_selected': category.pk,
            }
    return render(request, 'women/index.html', context = data)

def show_tag_postlist(request, tag_slug):
    # прочитаем пост из модели TagPost по слагу tag_slug
    tag = get_object_or_404(TagPost, slug = tag_slug)
    #берем все статьи кт связаны с этим тэгом
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
    data = {
        'title': f'Тэг: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
        }
    return render(request, 'women/index.html', context=data)

def addpage(request):
    # функция представления проверяет заполнена ли форма
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        # проверяем корретность заполнения (например чтобы slug был уникальным )
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        # иначе пришел GET запрос и отображаем форму с пустыми данными
        form = AddPostForm()

    data = {
        'menu': menu,
        'title': 'Добавление статьи',
        'form': form
    }
    return render(request, 'women/addpage.html', data)

def contact(request):
    return HttpResponse(f"Обратная связь")

def login(request):
    return HttpResponse(f"Авторизация")

def page_not_found(request, exception):
    return HttpResponseNotFound(f"<h1>Страница не найдена</h1>")

