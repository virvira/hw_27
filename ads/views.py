from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Advertisement, User, Location
from django.views.decorators.csrf import csrf_exempt

from ads.serializers import UserListSerializer, UserDetailSerializer, UserCreateSerializer, UserUpdateSerializer, \
    UserDestroySerializer, LocationSerializer, AdListSerializer, CategorySerializer, AdDetailSerializer, \
    AdCreateSerializer, AdUpdateSerializer, AdDestroySerializer
from hw27 import settings


def index(request):
    return JsonResponse("OK", safe=False, status=200)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AdvertisementListView(ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdListSerializer

    def list(self, request, *args, **kwargs):
        category = request.GET.get("cat", None)
        if category:
            self.queryset = Advertisement.objects.filter(
                category_id=category
            )

        search_word = request.GET.get("text", None)
        if search_word:
            self.queryset = Advertisement.objects.filter(
                description__icontains=search_word
            )

        location = request.GET.get("location", None)
        if location:
            self.queryset = Advertisement.objects.filter(
                author__locations__name__icontains=location
            )

        price_from = request.GET.get("price_from", None)
        price_to = request.GET.get("price_to", None)
        if price_from and price_to:
            self.queryset = Advertisement.objects.filter(
                price__range=(price_from, price_to)
            )

        return super().list(request, *args, **kwargs)


class AdvertisementDetailView(RetrieveAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdDetailSerializer


class AdvertisementCreateView(CreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdCreateSerializer


class AdvertisementUpdateView(UpdateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdUpdateSerializer


@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementImageUpdateView(UpdateView):
    model = Advertisement
    fields = ["name", "author", "price", "description", "is_published", "image", "category"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES["image"]
        self.object.save()

        return JsonResponse(
            {
                "id": self.object.id,
                "name": self.object.name,
                "image": self.object.image.url if self.object.image else None
            }
        )


class AdvertisementDeleteView(DestroyAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdDestroySerializer


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
