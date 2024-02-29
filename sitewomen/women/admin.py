from django.contrib import admin
from .models import Women, Category
@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    # отображаем поля, которые будут видны в админке
    list_display = ('id','title','time_create','cat','is_published')
    # указаваем поля кт будут кликабельны в админке
    list_display_links = ('id','title')
    # указаваем последовательность сортировки записей
    ordering = ('time_create','title')
    # указаваем поля кт можно изменить, при этом они не должны тогда быть кликабельными
    list_editable = ('is_published',)
    # пагинация списка записей (сколько показывать на странице)
    list_per_page = 4

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_display_links = ('id','name')
    ordering = ('name',)

# admin.site.register(Women, WomenAdmin)
# Register your models here.
