from rest_framework.permissions import BasePermission

from ads.models import User


class IsSelectionOwner(BasePermission):
    message = "This selection doesn't belong to the user"

    def has_object_permission(self, request, view, selection):
        if request.user == selection.owner:
            return True
        return False


class AdvertisementEditPermission(BasePermission):
    message = "No access"

    def has_object_permission(self, request, view, ad):
        if (request.user == ad.author
                or request.user.role != User.MEMBER):
            return True
        return False
