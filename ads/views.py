import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from ads.models import Category, Advertisement
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return JsonResponse("OK", safe=False, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()

        response = []

        for category in categories:
            response.append(
                {
                    "id": category.id,
                    "name": category.name
                }
            )

        return JsonResponse(response, safe=False)

    def post(self, request):
        category_data = json.loads(request.body)

        category = Category()
        category.name = category_data.get("name")

        try:
            category.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        category.save()
        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


class CategoryEntityView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, id=pk)

        return JsonResponse(
            {
                "id": category.id,
                "name": category.name
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementView(View):
    def get(self, request):
        ads = Advertisement.objects.all()

        response = []

        for ad in ads:
            response.append(
                {
                    "id": ad.id,
                    "name": ad.name,
                    "author": ad.author,
                    "price": ad.price,
                    "description": ad.description,
                    "address": ad.address,
                    "is_published": ad.is_published
                }
            )

        return JsonResponse(response, safe=False)

    def post(self, request):
        ad_data = json.loads(request.body)

        ad = Advertisement()
        ad.name = ad_data.get("name")
        ad.author = ad_data.get("author")
        ad.price = ad_data.get("price")
        ad.description = ad_data.get("description")
        ad.address = ad_data.get("address")
        ad.is_published = ad_data.get("is_published")

        try:
            ad.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        ad.save()
        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published
        })


class AdvertisementEntityView(View):
    def get(self, request, pk):
        ad = get_object_or_404(Advertisement, id=pk)

        return JsonResponse(
            {
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published
            }
        )
