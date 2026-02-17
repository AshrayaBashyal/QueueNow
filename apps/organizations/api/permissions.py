from rest_framework import permissions
from ..models import Membership

class IsOrgAdminOrReadOnly(permissions.BasePermission):
    """
    Allow anyone to see (GET), but only Org Admins to Edit/Delete.
    """
    def has_object_permission(self, request, view, obj):
        # Allow 'Safe' methods (GET, HEAD, OPTIONS) for all
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.memberships.filter(
            user=request.user, 
            role=Membership.Role.ADMIN
        ).exists()
