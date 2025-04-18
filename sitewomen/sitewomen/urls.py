from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from sitewomen import settings
from women.views import *

# class MyCustomRouter(routers.SimpleRouter):
#     routers = [
#         routers.Route(
#             url=r'^{prefix}$',
#             mapping={'get': 'list'},
#             name='{basename}-list',
#             detail=False,
#             initkwargs={'suffix': 'List'}),
#         routers.Route(
#             url=r'^{prefix}/{lookup}$',
#             mapping={'get': 'retrieve'},
#             name='{basename}-detail',
#             detail=True,
#             initkwargs={'suffix': 'Detail'})]

#router = routers.DefaultRouter() # класс роутеров формирует список маршрутов
# router = MyCustomRouter() # класс роутеров формирует список маршрутов
# router.register(r'ladies',WomenViewSet) # GET /api/v1/ladies/women-list/ имя маршрута берется из имени модели
# # router.register(r'women',WomenViewSet, basename = 'men') # GET /api/v1/women/men-list/ имя маршрута сменяется
# # модели
# print(router.urls)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/', include(router.urls)),
    path('', include('women.urls')),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/women', WomenAPIList.as_view()),
    path('api/v1/women/<int:pk>', WomenAPIUpdate.as_view()),
    path('api/v1/womendelete/<int:pk>', WomenAPIDestroy.as_view()),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),    # jwt token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   # jwt token
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),      # jwt token
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    # маршрут к медиафайлам в режиме отладки. В боевом режиме сервер сам знает путь
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Известные женщины мира"

