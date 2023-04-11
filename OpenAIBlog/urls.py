from decouple import config
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

admin_url = config('ADMIN_URL', default='gimsap_admin_dont_url')
urlpatterns = [
    path('', include('blog.urls'), name='blog'),
    path(f'{admin_url}/', admin.site.urls, name='admin'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
