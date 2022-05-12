from rest_framework import permissions

class AuthorModifyOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        """
        Anonymous users can read, author and superuser can read/write.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return (request.user == obj.author) or request.user.is_superuser

class IsObjectAdmin(permissions.IsAdminUser):
    """
    Has Admin permission on the object.
    """
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff)