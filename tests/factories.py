import factory.django

from ads.models import User, Advertisement, Category, Location, Selection


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("name")
    slug = factory.Faker("slug")


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Advertisement

    name = factory.Faker("name")
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(UserFactory)
    price = 300


class SelectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Selection

    name = factory.Faker("name")
    owner = factory.SubFactory(UserFactory)
    items = []
