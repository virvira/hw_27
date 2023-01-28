from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from ads import views
from hw27 import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('', include('ads.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

