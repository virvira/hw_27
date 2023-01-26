from django.contrib import admin

from ads.models import Advertisement
from ads.models import Category
from ads.models import User
from ads.models import Location

admin.site.register(Advertisement)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Location)
