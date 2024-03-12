from django.urls import path, register_converter
from . import converters
from . import views

register_converter(converters.FourDigitYearConverter,'year4')

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='addpage'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
]