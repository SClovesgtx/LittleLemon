from rest_framework import permissions


class OnlyGETPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.user.groups.filter(name="Customer").exists()
            or request.user.groups.filter(name="delivery crew").exists()
        ):
            return request.method == "GET"
        return True


class OnlyManagerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="Manager").exists():
            return True
        return False


class OnlyCustomerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # the customer is in any group
        if not request.user.groups.all():
            return True
        return False
