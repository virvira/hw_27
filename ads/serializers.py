from rest_framework import serializers

from ads.models import User, Location, Category, Advertisement


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all"


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
        fields = '__all__'


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

    class Meta:
        model = User
        fields = "__all__"

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        for location in self._locations:
            location_obj, _ = Location.objects.get_or_create(name=location)
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
