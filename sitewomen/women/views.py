from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView

from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost, UploadFiles



menu = [
    {'title': 'О сайте', 'url_name': "about"},
    {'title': "Добавить статью", 'url_name': "addpage"},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'}
]

# def index(request):
#     posts = Women.published.all().select_related('cat')
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=data)

class WomenHome(ListView):
    # предполагает получыение данных из таблицы
    template_name = 'women/index.html'
    model = Women
    context_object_name = 'posts'
    # определяем переменную  кт будет содержать список статей
    extra_context = {
        # этот словарь для статических данных
        'title': 'главная страница',
        'menu': menu,
        'cat_selected': 0,
        }

    def get_queryset(self):
        return Women.published.all().select_related('cat')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'главная страница'
    #     context['menu'] = menu
    #     context['posts'] = Women.published.all().select_related('cat')  # получение всех записей из модели Women
    #     context['cat_selected'] = int(self.request.GET.get('cat_id',0))
    #     return context


def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'women/about.html', {'title':'О сайте', 'menu': menu, 'form': form})

def show_post(request, post_slug):
    post = get_object_or_404(Women, slug = post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
        }
    return render(request, 'women/post.html', data)

# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug = cat_slug)
#     posts = Women.published.filter(cat_id = category.pk).select_related('cat')
#     data = {'title': f'Рубрика: {category.name}',
#             'menu': menu,
#             'posts': posts,
#             'cat_selected': category.pk,
#             }
#     return render(request, 'women/index.html', context = data)

class WomenCategory(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False # позволить пустой список категорий (отображается ошибка 404)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        print(cat)
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')



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

class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        data = {'menu': menu, 'title': 'Добавление статьи', 'form': form}
        return render(request, 'women/addpage.html', data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
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

