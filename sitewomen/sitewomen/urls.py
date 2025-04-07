from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from sitewomen import settings
from women.views import page_not_found, WomenAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/womenlist/', WomenAPIView.as_view()),
    path('', include('women.urls')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    # маршрут к медиафайлам в режиме отладки. В боевом режиме сервер сам знает путь
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Известные женщины мира"

