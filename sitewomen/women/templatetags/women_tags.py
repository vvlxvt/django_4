from django import template
from django.db.models import Count
from women.models import Category, TagPost
from women.utils import menu

register = template.Library()

@register.simple_tag
def get_menu():
    return menu

@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
    # показывает только те посты которые имеют категорию
    cats = Category.objects.annotate(total=Count('posts')).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}\

@register.inclusion_tag('women/list_tags.html')
def show_all_tags(cat_selected=0):
    # показывает только те тэги для которых есть соответствие
    return {'tags': TagPost.objects.annotate(total=Count('tags')).filter(total__gt=0)}