from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # get the user from the object (course or lesson)
        owner = obj.created_by if hasattr(obj, 'created_by') else obj.course.created_by

        # Write permissions are only allowed to the owner of the object.
        return owner == request.user