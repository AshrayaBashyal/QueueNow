from django.db import transaction
from ..models import Organization, Membership, Invite
from django.contrib.auth import get_user_model

User = get_user_model()


class InviteService:
    
    @staticmethod
    @transaction.atomic
    def send_invites(organization, invitee_email, inviter, role=Membership.Role.STAFF):

        if not inviter.memberships.filter(organization=organization, role=Membership.Role.ADMIN).exists():
            raise PermissionError("Only ADMIN can send invite")
        try:
            user_to_invite = User.objects.get(email=invitee_email)    
        except User.DoesNotExist:
            raise ValueError("User must be registered to receive an invite.")

        if organization.memberships.filter(user=user_to_invite).exists():
            raise ValueError("User is already a member of this organization.")
                
        if Invite.objects.filter(organization=organization, email=invitee_email, status='PENDING').exists():
            raise ValueError("An invitation is already pending for this user.")

        return Invite.objects.create(
            organization=organization,
            email=invitee_email,
            invited_by=inviter,
            role=role
        )            

