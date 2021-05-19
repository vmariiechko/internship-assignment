from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticatedOrViewOnly(BasePermission):
    """
    Allows to read for any request,
    but only authenticated users can change objects.
    """

    message = 'Modifying SMSes is allowed to the author only'

    def has_permission(self, request, view):

        # Allow to create, update and delete only for authenticated users
        if view.action in ['create', 'update', 'destroy']:
            return request.user and request.user.is_authenticated
        else:
            return True

    def has_object_permission(self, request, view, obj):

        # Allow reading an object for GET, HEAD, OPTIONS requests
        if request.method in SAFE_METHODS:
            return True

        # Only the owner can modify an object
        return obj.author == request.user
