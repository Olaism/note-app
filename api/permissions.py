from rest_framework import permissions

class IsNoteCreator(permissions.BasePermission):
    """
        Custom Permission to allow only owners of an object to edit it
    """
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user