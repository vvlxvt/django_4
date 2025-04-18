from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published = Women.Status.PUBLISHED)

class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'
    # verbose_name - подробное имя которое отоборажется в админке и других случая
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Слаг")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None, blank=True, null=True, verbose_name='Фото')
    content = models.TextField(blank=True, verbose_name='Статья')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="создано")
    time_update = models.DateTimeField(auto_now=True, verbose_name="изменено")
    # преобразуем последовательность choices в булевый тип, в Джанго есть только IntegerChoices и TextChoices
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]),x[1]), Status.choices)),
    default=Status.DRAFT, verbose_name="Статус")
    cat = models.ForeignKey('Category', on_delete = models.PROTECT, related_name='posts',verbose_name="Категория")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name="Тэг")
    # related_name - менеджеор обратного связывания
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True,  related_name =
    'wife', verbose_name="Муж")
    author = models.ForeignKey(get_user_model(), on_delete = models.SET_NULL, related_name='posts', null=True,
                                default=None )

    objects = models.Manager() # определяю модельные менеджеры
    published = PublishedManager()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'

        ordering = ['time_create']
        indexes = [models.Index(fields = ['time_create'])]

    def get_absolute_url(self):
        return reverse('post', kwargs = {'post_slug':self.slug})

    '''def save(self, *args, **kwargs):
        # определяем slug самостоятельно
        # альтернатива методу prepopulated_fields в модели
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)'''


class Category(models.Model):
    name = models.CharField(max_length = 100, db_index = True)
    slug = models.CharField(max_length = 100, db_index = True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index = True)
    slug = models.SlugField(max_length=100, unique = True, db_index = True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

class Husband(models.Model):
    name = models.CharField(max_length = 100)
    age = models.IntegerField(null = True)
    # blank = True - значит необязательное значение
    m_count = models.IntegerField(blank = True, default = 0)

    def __str__(self):
        return self.name

class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')




