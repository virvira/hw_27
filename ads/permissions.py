from rest_framework.permissions import BasePermission

from ads.models import User


class IsSelectionOwner(BasePermission):
    message = "This selection doesn't belong to the user"

    def has_object_permission(self, request, view, selection):
        if request.user == selection.owner:
            return True
        return False


# class IsAdmin(BasePermission):
#     message = "No access"
#
#     def has_permission(self, request, view):
#         if (request.user.role == User.MODERATOR or
#                 request.user.role == User.ADMIN):
#             return True
#         return False
#
#
# class IsAdvertisementAuthor(BasePermission):
#     message = "This ad doesn't belong to the user"
#
#     def has_object_permission(self, request, view, ad):
#         print(request.user)
#         print(ad.author)
#         if request.user == ad.author:
#             return True
#         return False


class AdvertisementEditPermission(BasePermission):
    message = "No access"

    def has_object_permission(self, request, view, ad):
        if (request.user == ad.author
                or request.user.role == User.MODERATOR
                or request.user.role == User.ADMIN):
            return True
        return False
