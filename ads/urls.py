from django.contrib import admin
from django.urls import path
from ads import views

urlpatterns = [
    path('cat/', views.CategoryListView.as_view(), name='category_all'),
    path('cat/<int:pk>/', views.CategoryDetailView.as_view(), name='category_by id'),
    path('cat/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('cat/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('cat/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),

    path('ad/', views.AdvertisementListView.as_view(), name='advertisement_all'),
    path('ad/<int:pk>/', views.AdvertisementDetailView.as_view(), name='advertisement_by_id'),
    path('ad/create/', views.AdvertisementCreateView.as_view(), name='advertisement_create'),
    path('ad/<int:pk>/update/', views.AdvertisementUpdateView.as_view(), name='advertisement_update'),
    path('ad/<int:pk>/upload_image/', views.AdvertisementImageUpdateView.as_view(), name='advertisement_image'),
    path('ad/<int:pk>/delete/', views.AdvertisementDeleteView.as_view(), name='advertisement_delete'),

    path('user/', views.UserListView.as_view(), name='user_all'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user_by_id'),
    path('user/create/', views.UserCreateView.as_view(), name='user_create'),
    path('user/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('user/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
]
