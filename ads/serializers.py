from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from ads.models import User, Location, Category, Advertisement, Selection


class NotAdIsPublishedFalseValidator:
    def __call__(self, is_published):
        if not is_published:
            raise serializers.ValidationError("Incorrect status")


class NotUserEmailInForbiddenList:
    def __init__(self, domain_list):
        self.domain_list = domain_list

    def __call__(self, email):
        for domain in self.domain_list:
            if domain in email:
                raise serializers.ValidationError("Incorrect email")


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"


class UserLocationSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = User
        fields = ["username", "locations"]


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class UserDetailSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = User
        fields = "__all__"


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=User.objects.all(),
        slug_field="name"
    )
    email = serializers.EmailField(validators=[NotUserEmailInForbiddenList(["rambler.ru"])])

    class Meta:
        model = User
        fields = "__all__"

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("locations", [])
        print(self._locations)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        for location in self._locations:
            print(location)
            location_obj, _ = Location.objects.get_or_create(name=location)
            print(location_obj)
            user.locations.add(location_obj)

        user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=User.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "password", "role", "age", "locations"]

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()

        for location in self._locations:
            location_obj, _ = Location.objects.get_or_create(name=location)
            user.locations.add(location_obj)

        user.save()
        return user


class UserDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id"]


class AdListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Category.objects.all()
    )

    author = UserLocationSerializer()

    class Meta:
        model = Advertisement
        fields = ["name", "price", "category", "author", "description"]


class AdDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Category.objects.all()
    )
    author = UserLocationSerializer()

    class Meta:
        model = Advertisement
        fields = ["name", "price", "category", "author", "description"]


class AdCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    category = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Category.objects.all()
    )
    author = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all()
    )
    is_published = serializers.BooleanField(validators=[NotAdIsPublishedFalseValidator()])

    class Meta:
        model = Advertisement
        exclude = ["image"]


class AdUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Category.objects.all()
    )
    author = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all()
    )

    class Meta:
        model = Advertisement
        exclude = ["image"]


class AdDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = Advertisement
        fields = ["id"]


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id", "name"]


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = AdListSerializer(
        many=True
    )

    class Meta:
        model = Selection
        fields = "__all__"


class SelectionCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    items = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Advertisement.objects.all(),
        slug_field="id"
    )

    class Meta:
        model = Selection
        fields = "__all__"

    def is_valid(self, raise_exception=False):
        self._items = self.initial_data.pop("items", [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        selection = Selection.objects.create(**validated_data)

        for item in self._items:
            item_obj = get_object_or_404(Advertisement, id=item)
            if item_obj:
                selection.items.add(item_obj)

        selection.save()

        return selection


class SelectionUpdateSerializer(serializers.ModelSerializer):
    items = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Advertisement.objects.all(),
        slug_field="id"
    )

    class Meta:
        model = Selection
        fields = ["id", "name", "owner", "items"]

    def is_valid(self, raise_exception=False):
        self._items = self.initial_data.pop("items", [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        selection = super().save()

        for item in self._items:
            item_obj = get_object_or_404(Advertisement, id=item)
            if item_obj:
                selection.items.add(item_obj)

        selection.save()
        return selection


class SelectionDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = Selection
        fields = ["id"]
