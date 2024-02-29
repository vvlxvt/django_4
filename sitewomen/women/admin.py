from django.contrib import admin
from .models import Women, Category
@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    # отображаем поля, которые будут видны в админке
    list_display = ('title','time_create','cat','is_published', 'brief_info')
    # указаваем поля кт будут кликабельны в админке
    list_display_links = ('title',)
    # указаваем последовательность сортировки записей
    ordering = ('time_create','title')
    # указаваем поля кт можно изменить, при этом они не должны тогда быть кликабельными
    list_editable = ('is_published',)
    # пагинация списка записей (сколько показывать на странице)
    list_per_page = 4

    @admin.display(description='Краткое описание', ordering= 'content')
    def brief_info(self, women: Women):
        return f'Описание {len(women.content)} символов'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_display_links = ('id','name')
    ordering = ('name',)

# admin.site.register(Women, WomenAdmin)
# Register your models here.
