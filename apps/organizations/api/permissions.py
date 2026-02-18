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

        is_admin = obj.memberships.filter(
            user=request.user, 
            role=Membership.Role.ADMIN
        ).exists()

        if is_admin:
            return True
        
        if request.method in ["PUT", "PATCH"]:
            return obj.memberships.filter(
                user=request.user,
                role=Membership.Role.STAFF
            ).exists()

        return False
    
    
    # using obj.memberships.filter twice, hitting the database twice for every edit request from a Staff member. Can fetch the role once, but for now, this code is very readable and safe.
