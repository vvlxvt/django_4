from django.contrib import admin, messages
from .models import Women, Category

class MarriedFilter(admin.SimpleListFilter):
    # новый фильтр для админ панели
    title = 'Статус женщин'
    # значение перемнной в запросе http://127.0.0.1:8000/admin/women/women/?status=single
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        # возвращает список возможных значений параметра status
        return [('married', 'замужем'),
        ('single', 'не замужем'),]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            # self.value() возвращает значение параметра status
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)
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
    # добавляем новое действие
    actions = ['set_published', 'set_draft']
    search_fields = ('title','cat__name',)
    list_filter = (MarriedFilter,'cat__name', 'is_published')

    @admin.display(description='Краткое описание', ordering= 'content')
    # добавляем дополнительное поле к записям в админку
    def brief_info(self, women: Women):
        return f'Описание {len(women.content)} символов'

    @admin.action(description='Опубликовать выбранные записи')
    # добавляем действие к выбранным записям в админку
    def set_published(self, request, queryset):
        count = queryset.update(is_published = Women.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей')    \

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published = Women.Status.DRAFT)
        self.message_user(request, f'{count} записей снято с публикации', messages.WARNING)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_display_links = ('id','name')
    ordering = ('name',)

# admin.site.register(Women, WomenAdmin)
# Register your models here.
