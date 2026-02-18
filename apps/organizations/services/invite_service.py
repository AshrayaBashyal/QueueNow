from django.db import transaction
from ..models import Organization, Membership, Invite
from django.contrib.auth import get_user_model

User = get_user_model()


class InviteService:
    
    @staticmethod
    @transaction.atomic
    def send_invites(*, organization, inviter, invitee_email=None, invitee_id=None, role=Membership.Role.STAFF):

        if not inviter.memberships.filter(organization=organization, role=Membership.Role.ADMIN).exists():
            raise PermissionError("Only ADMIN can send invite")
        
        user_to_invite = None
        if invitee_id:
            user_to_invite = User.objects.filter(id=invitee_id).first()
        elif invitee_email:
            user_to_invite = User.objects.filter(email=invitee_email).first() 

        if not user_to_invite:
            raise ValueError("User must be registered to receive an invite.")

        if organization.memberships.filter(user=user_to_invite).exists():
            raise ValueError("User is already a member of this organization.")
                
        if Invite.objects.filter(organization=organization, invitee=user_to_invite , status='PENDING').exists():
            raise ValueError("An invitation is already pending for this user.")

        return Invite.objects.create(
            organization=organization,
            invitee=user_to_invite,
            email=user_to_invite.email,
            invited_by=inviter,
            role=role
        )            


    @staticmethod
    def cancel_invite(*, invite, cancelled_by):
        """
        Logic: Only the original inviter OR the Org Admin can cancel a pending invite.
        """
        is_inviter = invite.invited_by == cancelled_by
        
        if not is_inviter:
            is_admin = invite.organization.memberships.filter(
                user=cancelled_by, 
                role=Membership.Role.ADMIN
            ).exists()
            
            if not is_admin:
                raise PermissionError("Only the inviter or an admin can cancel this invite.")

        # State check
        if invite.status != Invite.Status.PENDING:
            raise ValueError(f"Cannot cancel an invite that is already {invite.status.lower()}.")

        invite.status = Invite.Status.CANCELLED            
        invite.save()