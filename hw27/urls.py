from django.contrib import admin
from django.urls import path
from ads import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('cat/', views.CategoryView.as_view(), name='category'),
    path('cat/<int:pk>', views.CategoryEntityView.as_view(), name='category'),
    path('ad/', views.AdvertisementView.as_view(), name='advertisement'),
    path('ad/<int:pk>', views.AdvertisementEntityView.as_view(), name='advertisement')
]
