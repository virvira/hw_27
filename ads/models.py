from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=50)
    lat = models.DecimalField(decimal_places=7, max_digits=9)
    lng = models.DecimalField(decimal_places=7, max_digits=9)

    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположения"
        order_with_respect_to = "name"


class User(models.Model):
    ROLE = [
        ("member", "Базовый пользователь"),
        ("moderator", "Модератор"),
        ("admin", "Администратор"),
    ]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=15, default="member", choices=ROLE)
    age = models.PositiveSmallIntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        order_with_respect_to = "username"


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        order_with_respect_to = "name"


class Advertisement(models.Model):
    name = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.CharField(max_length=500)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to="images/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        order_with_respect_to = "name"

