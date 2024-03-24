from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost, UploadFiles
from .utils import DataMixin

class WomenHome(DataMixin, ListView):
    # предполагает получыение данных из таблицы
    template_name = 'women/index.html'
    title_page = 'Главная страница'
    paginate_by = 3
    cat_selected = 0
    model = Women
    context_object_name = 'posts'
    # определяем переменную  кт будет содержать список статей

    def get_queryset(self):
        return Women.published.all().select_related('cat')

@login_required(login_url = '/admin/')
def about(request):
    contact_list=Women.published.all()
    paginator = Paginator(contact_list,3) # класс Paginator содержащий список опубликованных объектов с просмотром по 3
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'women/about.html', {'title':'О сайте', 'page_obj': page_obj})


class ShowPost(DataMixin,DetailView):
    template_name = 'women/post.html' # имя вашего шаблона
    slug_url_kwarg = 'post_slug'   # переменная которая фигурирует в маршруте
    context_object_name = 'post' #  имя объекта в контексте шаблона
    # присваеиваем переменной контекста object ранее использованное в post.html имя post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title = context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug = self.kwargs[self.slug_url_kwarg])


class WomenCategory(DataMixin,ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False # позволить пустой список категорий (отображается ошибка 404)

    def get_queryset(self):
        result = Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')
        print(result)
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.pk)


class TagPostList(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug = self.kwargs['tag_slug'])
        context['title'] = 'Тэг - ' + tag.tag
        return self.get_mixin_context(context, title='Тэг - ' + tag.tag)

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

class AddPage(DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    title_page = 'Добавление статьи'
    # login_url = '/admin/' # адрес перенаправления неавторизованого пользователя

    def form_valid(self, form):
        w=form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)



class UpdatePage(DataMixin, UpdateView):
    title_page = 'Редактирование статьи'
    fields = ['title', 'content', 'photo','is_published','cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')


class DeletePage(DeleteView):
    model = Women
    template_name = 'women/post_confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('home')
    template_name_suffix = "_confirm_delete"
    pk_url_kwarg = 'pk'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, pk = self.kwargs[self.pk_url_kwarg])

def contact(request):
    return HttpResponse(f"Обратная связь")

def login(request):
    return HttpResponse(f"Авторизация")

def page_not_found(request, exception):
    return HttpResponseNotFound(f"<h1>Страница не найдена</h1>")

