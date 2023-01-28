import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from ads.models import Category, Advertisement, User, Location
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt

from hw27 import settings


def index(request):
    return JsonResponse("OK", safe=False, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by('name')

        response = []
        for category in self.object_list:
            response.append(
                {
                    "id": category.id,
                    "name": category.name
                }
            )
        return JsonResponse(response, safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse(
            {
                "id": self.object.id,
                "name": self.object.name
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)
        category, _ = Category.objects.get_or_create(name=category_data["name"])
        return JsonResponse(
            {
                "id": category.id,
                "name": category.name
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        cat_data = json.loads(request.body)
        self.object.name = cat_data["name"]
        self.object.save()

        return JsonResponse(
            {
                "id": self.object.id,
                "name": self.object.name
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementListView(ListView):
    model = Advertisement

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by('-price')

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        ads = []
        for ad in page_obj:
            ads.append(
                {
                    "id": ad.id,
                    "name": ad.name,
                    "author": ad.author.id,
                    "price": ad.price,
                    "description": ad.description,
                    "is_published": ad.is_published,
                    "image": ad.image.url if ad.image else None,
                    "category": ad.category.id
                }
            )

        response = {
            "items": ads,
            "num_pages": paginator.num_pages,
            "total_count": paginator.count
        }
        return JsonResponse(response, safe=False)


class AdvertisementDetailView(DetailView):
    model = Advertisement

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse(
            {
                "id": self.object.id,
                "name": self.object.name,
                "author": self.object.author.id,
                "price": self.object.price,
                "description": self.object.description,
                "is_published": self.object.is_published,
                "image": self.object.image.url if self.object.image else None,
                "category": self.object.category.id
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementCreateView(CreateView):
    model = Advertisement
    fields = ["name", "author", "price", "description", "is_published", "category"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        ad, _ = Advertisement.objects.get_or_create(
            name=ad_data["name"],
            author_id=ad_data["author"],
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
            category_id=ad_data["category"]
        )

        return JsonResponse(
            {
                "id": ad.id,
                "name": ad.name,
                "author": ad.author.id,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "image": self.object.image.url if self.object.image else None,
                "category": ad.category.id
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementUpdateView(UpdateView):
    model = Advertisement
    fields = ["name", "author", "price", "description", "is_published", "category"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        self.object.name = ad_data["name"]
        self.object.author_id = ad_data["author"]
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]
        self.object.category_id = ad_data["category"]

        self.object.save()

        return JsonResponse(
            {
                "id": self.object.id,
                "name": self.object.name,
                "author_id": self.object.author.id,
                "author": self.object.author.first_name,
                "price": self.object.price,
                "description": self.object.description,
                "is_published": self.object.is_published,
                "image": self.object.image.url if self.object.image else None,
                "category": self.object.category.id
            }
        )


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


@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementDeleteView(DeleteView):
    model = Advertisement
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append(
                {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "password": user.password,
                    "role": user.role,
                    "age": user.age,
                    "total_ads": user.advertisement_set.filter(is_published=True).count(),
                    "locations": list(user.locations.all().values_list("name", flat=True)),
                }
            )

        response = {
            "items": users,
            "num_pages": paginator.num_pages,
            "total_count": paginator.count
        }
        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse(
            {
                "id": self.object.id,
                "first_name": self.object.first_name,
                "last_name": self.object.last_name,
                "username": self.object.username,
                "password": self.object.password,
                "role": self.object.role,
                "age": self.object.age,
                "locations": list(self.object.locations.all().values_list("name", flat=True)),
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "location"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user, _ = User.objects.get_or_create(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            username=user_data["username"],
            password=user_data["password"],
            role=user_data["role"],
            age=user_data["age"]
        )

        for location in user_data["locations"]:
            try:
                location_obj = Location.objects.get(name=location)
            except Location.DoesNotExist:
                return JsonResponse({"error": "Location not found"}, status=404)
            user.locations.add(location_obj)

        return JsonResponse(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "age": user.age,
                "locations": list(user.locations.all().values_list("name", flat=True)),
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "locations"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)

        for location in user_data["locations"]:
            try:
                location_obj = Location.objects.get(name=location)
            except Location.DoesNotExist:
                return JsonResponse({"error": "Location not found"}, status=404)
            self.object.locations.add(location_obj)

        self.object.first_name = user_data["first_name"]
        self.object.last_name = user_data["last_name"]
        self.object.username = user_data["username"]
        self.object.password = user_data["password"]
        self.object.role = user_data["role"]
        self.object.age = user_data["age"]
        self.object.save()

        return JsonResponse(
            {
                "id": self.object.id,
                "first_name": self.object.first_name,
                "last_name": self.object.last_name,
                "username": self.object.username,
                "password": self.object.password,
                "role": self.object.role,
                "age": self.object.age,
                "locations": list(self.object.locations.all().values_list("name", flat=True)),
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
