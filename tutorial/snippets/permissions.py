# Really we'd like all code snippets to be visible to anyone, but also make sure that only the user that created a code snippet is able to update or delete it.
# To do that we're going to need to create a custom permission

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    # Custom permissions that only allow owners of an object to edit it
    def has_object_permisson(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
    
    