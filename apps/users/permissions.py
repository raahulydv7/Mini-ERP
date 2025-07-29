from rest_framework import permissions

class IsAdminOrManager(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager

class IsAdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class IsSalesExecutiveOrManager(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_manager:
            return True
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        return False