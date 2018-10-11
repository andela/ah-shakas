from rest_framework import permissions


class IsOwnerOrReadonly(permissions.BasePermission):
    """This class creates permissions for delete and update methods"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # We check if is owner if either user or author are 
        # related to the requqesst user.
        # Note: use of getattr to avoid AttributeError
        return request.user in [
            getattr(obj, 'user', None),
            getattr(obj, 'author', None), 
        ]
