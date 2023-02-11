from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ads import views
from rest_framework import routers

from ads.views import LocationViewSet, CategoryViewSet

router = routers.SimpleRouter()
router.register('location', LocationViewSet)
router.register('cat', CategoryViewSet)

urlpatterns = [
    path('ad/', views.AdvertisementListView.as_view(), name='advertisement_all'),
    path('ad/<int:pk>/', views.AdvertisementDetailView.as_view(), name='advertisement_by_id'),
    path('ad/create/', views.AdvertisementCreateView.as_view(), name='advertisement_create'),
    path('ad/<int:pk>/update/', views.AdvertisementUpdateView.as_view(), name='advertisement_update'),
    # path('ad/<int:pk>/upload_image/', views.AdvertisementImageUpdateView.as_view(), name='advertisement_image'),
    path('ad/<int:pk>/delete/', views.AdvertisementDeleteView.as_view(), name='advertisement_delete'),

    path('user/', views.UserListView.as_view(), name='user_all'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user_by_id'),
    path('user/create/', views.UserCreateView.as_view(), name='user_create'),
    path('user/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('user/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('user/token/', TokenObtainPairView.as_view(), name='user_token'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='user_refresh_token'),

    path('selection/', views.SelectionListView.as_view(), name='selection_all'),
    path('selection/<int:pk>/', views.SelectionDetailView.as_view(), name='selection_by_id'),
    path('selection/create/', views.SelectionCreateView.as_view(), name='user_create'),
    path('selection/<int:pk>/update/', views.SelectionUpdateView.as_view(), name='selection_update'),
    path('selection/<int:pk>/delete/', views.SelectionDeleteView.as_view(), name='selection_delete'),

    path('', include(router.urls))
]
