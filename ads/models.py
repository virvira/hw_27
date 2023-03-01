# import uuid
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models


def check_birthdate(value: date):
    if value > date.today() - relativedelta(years=9):
        raise ValidationError(
            'The user is too young',
            params={'value': value},
        )


class Location(models.Model):
    name = models.CharField(max_length=50)
    lat = models.DecimalField(decimal_places=7, max_digits=9)
    lng = models.DecimalField(decimal_places=7, max_digits=9)

    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name


class User(AbstractUser):
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"
    ROLE = [
        (MEMBER, "Базовый пользователь"),
        (MODERATOR, "Модератор"),
        (ADMIN, "Администратор"),
    ]

    role = models.CharField(max_length=15, default="member", choices=ROLE)
    age = models.PositiveSmallIntegerField(null=True)
    locations = models.ManyToManyField(Location)
    birthdate = models.DateField(validators=[check_birthdate], null=True)
    email = models.EmailField(unique=True, null=True)

    # def save(self, *args, **kwargs):
    #     self.set_password(self.password)
    #     return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(5)]
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Advertisement(models.Model):
    name = models.CharField(max_length=150, null=False, validators=[MinLengthValidator(10)])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    description = models.CharField(max_length=500, null=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to="images/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name


class Selection(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Advertisement)

    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"

    def __str__(self):
        return self.name
